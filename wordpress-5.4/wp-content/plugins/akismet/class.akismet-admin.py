#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
class Akismet_Admin():
    NONCE = "akismet-update-key"
    initiated = False
    notices = Array()
    allowed = Array({"a": Array({"href": True, "title": True})}, {"b": Array(), "code": Array(), "del": Array({"datetime": True})}, {"em": Array(), "i": Array(), "q": Array({"cite": True})}, {"strike": Array(), "strong": Array()})
    @classmethod
    def init(self):
        
        
        if (not self.initiated):
            self.init_hooks()
        # end if
        if (php_isset(lambda : PHP_POST["action"])) and PHP_POST["action"] == "enter-key":
            self.enter_api_key()
        # end if
        if (not php_empty(lambda : PHP_REQUEST["akismet_comment_form_privacy_notice"])) and php_empty(lambda : PHP_REQUEST["settings-updated"]):
            self.set_form_privacy_notice_option(PHP_REQUEST["akismet_comment_form_privacy_notice"])
        # end if
    # end def init
    @classmethod
    def init_hooks(self):
        
        
        #// The standalone stats page was removed in 3.0 for an all-in-one config and stats page.
        #// Redirect any links that might have been bookmarked or in browser history.
        if (php_isset(lambda : PHP_REQUEST["page"])) and "akismet-stats-display" == PHP_REQUEST["page"]:
            wp_safe_redirect(esc_url_raw(self.get_page_url("stats")), 301)
            php_exit(0)
        # end if
        self.initiated = True
        add_action("admin_init", Array("Akismet_Admin", "admin_init"))
        add_action("admin_menu", Array("Akismet_Admin", "admin_menu"), 5)
        #// # Priority 5, so it's called before Jetpack's admin_menu.
        add_action("admin_notices", Array("Akismet_Admin", "display_notice"))
        add_action("admin_enqueue_scripts", Array("Akismet_Admin", "load_resources"))
        add_action("activity_box_end", Array("Akismet_Admin", "dashboard_stats"))
        add_action("rightnow_end", Array("Akismet_Admin", "rightnow_stats"))
        add_action("manage_comments_nav", Array("Akismet_Admin", "check_for_spam_button"))
        add_action("admin_action_akismet_recheck_queue", Array("Akismet_Admin", "recheck_queue"))
        add_action("wp_ajax_akismet_recheck_queue", Array("Akismet_Admin", "recheck_queue"))
        add_action("wp_ajax_comment_author_deurl", Array("Akismet_Admin", "remove_comment_author_url"))
        add_action("wp_ajax_comment_author_reurl", Array("Akismet_Admin", "add_comment_author_url"))
        add_action("jetpack_auto_activate_akismet", Array("Akismet_Admin", "connect_jetpack_user"))
        add_filter("plugin_action_links", Array("Akismet_Admin", "plugin_action_links"), 10, 2)
        add_filter("comment_row_actions", Array("Akismet_Admin", "comment_row_action"), 10, 2)
        add_filter("plugin_action_links_" + plugin_basename(plugin_dir_path(__FILE__) + "akismet.php"), Array("Akismet_Admin", "admin_plugin_settings_link"))
        add_filter("wxr_export_skip_commentmeta", Array("Akismet_Admin", "exclude_commentmeta_from_export"), 10, 3)
        add_filter("all_plugins", Array("Akismet_Admin", "modify_plugin_description"))
        if php_class_exists("Jetpack"):
            add_filter("akismet_comment_form_privacy_notice_url_display", Array("Akismet_Admin", "jetpack_comment_form_privacy_notice_url"))
            add_filter("akismet_comment_form_privacy_notice_url_hide", Array("Akismet_Admin", "jetpack_comment_form_privacy_notice_url"))
        # end if
        #// priority=1 because we need ours to run before core's comment anonymizer runs, and that's registered at priority=10
        add_filter("wp_privacy_personal_data_erasers", Array("Akismet_Admin", "register_personal_data_eraser"), 1)
    # end def init_hooks
    @classmethod
    def admin_init(self):
        
        
        if get_option("Activated_Akismet"):
            delete_option("Activated_Akismet")
            if (not php_headers_sent()):
                wp_redirect(add_query_arg(Array({"page": "akismet-key-config", "view": "start"}), admin_url("admin.php") if php_class_exists("Jetpack") else admin_url("options-general.php")))
            # end if
        # end if
        load_plugin_textdomain("akismet")
        add_meta_box("akismet-status", __("Comment History", "akismet"), Array("Akismet_Admin", "comment_status_meta_box"), "comment", "normal")
        if php_function_exists("wp_add_privacy_policy_content"):
            wp_add_privacy_policy_content(__("Akismet", "akismet"), __("We collect information about visitors who comment on Sites that use our Akismet anti-spam service. The information we collect depends on how the User sets up Akismet for the Site, but typically includes the commenter's IP address, user agent, referrer, and Site URL (along with other information directly provided by the commenter such as their name, username, email address, and the comment itself).", "akismet"))
        # end if
    # end def admin_init
    @classmethod
    def admin_menu(self):
        
        
        if php_class_exists("Jetpack"):
            add_action("jetpack_admin_menu", Array("Akismet_Admin", "load_menu"))
        else:
            self.load_menu()
        # end if
    # end def admin_menu
    @classmethod
    def admin_head(self):
        
        
        if (not current_user_can("manage_options")):
            return
        # end if
    # end def admin_head
    @classmethod
    def admin_plugin_settings_link(self, links_=None):
        
        
        settings_link_ = "<a href=\"" + esc_url(self.get_page_url()) + "\">" + __("Settings", "akismet") + "</a>"
        array_unshift(links_, settings_link_)
        return links_
    # end def admin_plugin_settings_link
    @classmethod
    def load_menu(self):
        
        
        if php_class_exists("Jetpack"):
            hook_ = add_submenu_page("jetpack", __("Akismet Anti-Spam", "akismet"), __("Akismet Anti-Spam", "akismet"), "manage_options", "akismet-key-config", Array("Akismet_Admin", "display_page"))
        else:
            hook_ = add_options_page(__("Akismet Anti-Spam", "akismet"), __("Akismet Anti-Spam", "akismet"), "manage_options", "akismet-key-config", Array("Akismet_Admin", "display_page"))
        # end if
        if hook_:
            add_action(str("load-") + str(hook_), Array("Akismet_Admin", "admin_help"))
        # end if
    # end def load_menu
    @classmethod
    def load_resources(self):
        
        
        global hook_suffix_
        php_check_if_defined("hook_suffix_")
        if php_in_array(hook_suffix_, apply_filters("akismet_admin_page_hook_suffixes", Array("index.php", "edit-comments.php", "comment.php", "post.php", "settings_page_akismet-key-config", "jetpack_page_akismet-key-config", "plugins.php"))):
            wp_register_style("akismet.css", plugin_dir_url(__FILE__) + "_inc/akismet.css", Array(), AKISMET_VERSION)
            wp_enqueue_style("akismet.css")
            wp_register_script("akismet.js", plugin_dir_url(__FILE__) + "_inc/akismet.js", Array("jquery"), AKISMET_VERSION)
            wp_enqueue_script("akismet.js")
            inline_js_ = Array({"comment_author_url_nonce": wp_create_nonce("comment_author_url_nonce"), "strings": Array({"Remove this URL": __("Remove this URL", "akismet"), "Removing...": __("Removing...", "akismet"), "URL removed": __("URL removed", "akismet"), "(undo)": __("(undo)", "akismet"), "Re-adding...": __("Re-adding...", "akismet")})})
            if (php_isset(lambda : PHP_REQUEST["akismet_recheck"])) and wp_verify_nonce(PHP_REQUEST["akismet_recheck"], "akismet_recheck"):
                inline_js_["start_recheck"] = True
            # end if
            wp_localize_script("akismet.js", "WPAkismet", inline_js_)
        # end if
    # end def load_resources
    #// 
    #// Add help to the Akismet page
    #// 
    #// @return false if not the Akismet page
    #//
    @classmethod
    def admin_help(self):
        
        
        current_screen_ = get_current_screen()
        #// Screen Content
        if current_user_can("manage_options"):
            if (not Akismet.get_api_key()) or (php_isset(lambda : PHP_REQUEST["view"])) and PHP_REQUEST["view"] == "start":
                #// setup page
                current_screen_.add_help_tab(Array({"id": "overview", "title": __("Overview", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Setup", "akismet") + "</strong></p>" + "<p>" + esc_html__("Akismet filters out spam, so you can focus on more important things.", "akismet") + "</p>" + "<p>" + esc_html__("On this page, you are able to set up the Akismet plugin.", "akismet") + "</p>"}))
                current_screen_.add_help_tab(Array({"id": "setup-signup", "title": __("New to Akismet", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Setup", "akismet") + "</strong></p>" + "<p>" + esc_html__("You need to enter an API key to activate the Akismet service on your site.", "akismet") + "</p>" + "<p>" + php_sprintf(__("Sign up for an account on %s to get an API Key.", "akismet"), "<a href=\"https://akismet.com/plugin-signup/\" target=\"_blank\">Akismet.com</a>") + "</p>"}))
                current_screen_.add_help_tab(Array({"id": "setup-manual", "title": __("Enter an API Key", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Setup", "akismet") + "</strong></p>" + "<p>" + esc_html__("If you already have an API key", "akismet") + "</p>" + "<ol>" + "<li>" + esc_html__("Copy and paste the API key into the text field.", "akismet") + "</li>" + "<li>" + esc_html__("Click the Use this Key button.", "akismet") + "</li>" + "</ol>"}))
            elif (php_isset(lambda : PHP_REQUEST["view"])) and PHP_REQUEST["view"] == "stats":
                #// stats page
                current_screen_.add_help_tab(Array({"id": "overview", "title": __("Overview", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Stats", "akismet") + "</strong></p>" + "<p>" + esc_html__("Akismet filters out spam, so you can focus on more important things.", "akismet") + "</p>" + "<p>" + esc_html__("On this page, you are able to view stats on spam filtered on your site.", "akismet") + "</p>"}))
            else:
                #// configuration page
                current_screen_.add_help_tab(Array({"id": "overview", "title": __("Overview", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Configuration", "akismet") + "</strong></p>" + "<p>" + esc_html__("Akismet filters out spam, so you can focus on more important things.", "akismet") + "</p>" + "<p>" + esc_html__("On this page, you are able to update your Akismet settings and view spam stats.", "akismet") + "</p>"}))
                current_screen_.add_help_tab(Array({"id": "settings", "title": __("Settings", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Configuration", "akismet") + "</strong></p>" + "" if Akismet.predefined_api_key() else "<p><strong>" + esc_html__("API Key", "akismet") + "</strong> - " + esc_html__("Enter/remove an API key.", "akismet") + "</p>" + "<p><strong>" + esc_html__("Comments", "akismet") + "</strong> - " + esc_html__("Show the number of approved comments beside each comment author in the comments list page.", "akismet") + "</p>" + "<p><strong>" + esc_html__("Strictness", "akismet") + "</strong> - " + esc_html__("Choose to either discard the worst spam automatically or to always put all spam in spam folder.", "akismet") + "</p>"}))
                if (not Akismet.predefined_api_key()):
                    current_screen_.add_help_tab(Array({"id": "account", "title": __("Account", "akismet"), "content": "<p><strong>" + esc_html__("Akismet Configuration", "akismet") + "</strong></p>" + "<p><strong>" + esc_html__("Subscription Type", "akismet") + "</strong> - " + esc_html__("The Akismet subscription plan", "akismet") + "</p>" + "<p><strong>" + esc_html__("Status", "akismet") + "</strong> - " + esc_html__("The subscription status - active, cancelled or suspended", "akismet") + "</p>"}))
                # end if
            # end if
        # end if
        #// Help Sidebar
        current_screen_.set_help_sidebar("<p><strong>" + esc_html__("For more information:", "akismet") + "</strong></p>" + "<p><a href=\"https://akismet.com/faq/\" target=\"_blank\">" + esc_html__("Akismet FAQ", "akismet") + "</a></p>" + "<p><a href=\"https://akismet.com/support/\" target=\"_blank\">" + esc_html__("Akismet Support", "akismet") + "</a></p>")
    # end def admin_help
    @classmethod
    def enter_api_key(self):
        
        
        if (not current_user_can("manage_options")):
            php_print(__("Cheatin&#8217; uh?", "akismet"))
            php_exit()
        # end if
        if (not wp_verify_nonce(PHP_POST["_wpnonce"], self.NONCE)):
            return False
        # end if
        for option_ in Array("akismet_strictness", "akismet_show_user_comments_approved"):
            update_option(option_, "1" if (php_isset(lambda : PHP_POST[option_])) and php_int(PHP_POST[option_]) == 1 else "0")
        # end for
        if (not php_empty(lambda : PHP_POST["akismet_comment_form_privacy_notice"])):
            self.set_form_privacy_notice_option(PHP_POST["akismet_comment_form_privacy_notice"])
        else:
            self.set_form_privacy_notice_option("hide")
        # end if
        if Akismet.predefined_api_key():
            return False
            pass
        # end if
        new_key_ = php_preg_replace("/[^a-f0-9]/i", "", PHP_POST["key"])
        old_key_ = Akismet.get_api_key()
        if php_empty(lambda : new_key_):
            if (not php_empty(lambda : old_key_)):
                delete_option("wordpress_api_key")
                self.notices[-1] = "new-key-empty"
            # end if
        elif new_key_ != old_key_:
            self.save_key(new_key_)
        # end if
        return True
    # end def enter_api_key
    @classmethod
    def save_key(self, api_key_=None):
        
        
        key_status_ = Akismet.verify_key(api_key_)
        if key_status_ == "valid":
            akismet_user_ = self.get_akismet_user(api_key_)
            if akismet_user_:
                if php_in_array(akismet_user_.status, Array("active", "active-dunning", "no-sub")):
                    update_option("wordpress_api_key", api_key_)
                # end if
                if akismet_user_.status == "active":
                    self.notices["status"] = "new-key-valid"
                elif akismet_user_.status == "notice":
                    self.notices["status"] = akismet_user_
                else:
                    self.notices["status"] = akismet_user_.status
                # end if
            else:
                self.notices["status"] = "new-key-invalid"
            # end if
        elif php_in_array(key_status_, Array("invalid", "failed")):
            self.notices["status"] = "new-key-" + key_status_
        # end if
    # end def save_key
    @classmethod
    def dashboard_stats(self):
        
        
        if did_action("rightnow_end"):
            return
            pass
        # end if
        count_ = get_option("akismet_spam_count")
        if (not count_):
            return
        # end if
        global submenu_
        php_check_if_defined("submenu_")
        php_print("<h3>" + esc_html(_x("Spam", "comments", "akismet")) + "</h3>")
        php_print("<p>" + php_sprintf(_n("<a href=\"%1$s\">Akismet</a> has protected your site from <a href=\"%2$s\">%3$s spam comment</a>.", "<a href=\"%1$s\">Akismet</a> has protected your site from <a href=\"%2$s\">%3$s spam comments</a>.", count_, "akismet"), "https://akismet.com/wordpress/", esc_url(add_query_arg(Array({"page": "akismet-admin"}), admin_url("edit-comments.php" if (php_isset(lambda : submenu_["edit-comments.php"])) else "edit.php"))), number_format_i18n(count_)) + "</p>")
    # end def dashboard_stats
    #// WP 2.5+
    @classmethod
    def rightnow_stats(self):
        
        
        count_ = get_option("akismet_spam_count")
        if count_:
            intro_ = php_sprintf(_n("<a href=\"%1$s\">Akismet</a> has protected your site from %2$s spam comment already. ", "<a href=\"%1$s\">Akismet</a> has protected your site from %2$s spam comments already. ", count_, "akismet"), "https://akismet.com/wordpress/", number_format_i18n(count_))
        else:
            intro_ = php_sprintf(__("<a href=\"%s\">Akismet</a> blocks spam from getting to your blog. ", "akismet"), "https://akismet.com/wordpress/")
        # end if
        link_ = add_query_arg(Array({"comment_status": "spam"}), admin_url("edit-comments.php"))
        queue_count_ = self.get_spam_count()
        if queue_count_:
            queue_text_ = php_sprintf(_n("There&#8217;s <a href=\"%2$s\">%1$s comment</a> in your spam queue right now.", "There are <a href=\"%2$s\">%1$s comments</a> in your spam queue right now.", queue_count_, "akismet"), number_format_i18n(queue_count_), esc_url(link_))
        else:
            queue_text_ = php_sprintf(__("There&#8217;s nothing in your <a href='%s'>spam queue</a> at the moment.", "akismet"), esc_url(link_))
        # end if
        text_ = intro_ + "<br />" + queue_text_
        php_print(str("<p class='akismet-right-now'>") + str(text_) + str("</p>\n"))
    # end def rightnow_stats
    @classmethod
    def check_for_spam_button(self, comment_status_=None):
        
        
        #// The "Check for Spam" button should only appear when the page might be showing
        #// a comment with comment_approved=0, which means an un-trashed, un-spammed,
        #// not-yet-moderated comment.
        if "all" != comment_status_ and "moderated" != comment_status_:
            return
        # end if
        link_ = add_query_arg(Array({"action": "akismet_recheck_queue"}), admin_url("admin.php"))
        comments_count_ = wp_count_comments()
        php_print("</div>")
        php_print("<div class=\"alignleft actions\">")
        classes_ = Array("button-secondary", "checkforspam")
        if (not Akismet.get_api_key()):
            link_ = admin_url("options-general.php?page=akismet-key-config")
            classes_[-1] = "checkforspam-pending-config"
        # end if
        if comments_count_.moderated == 0:
            classes_[-1] = "button-disabled"
        # end if
        php_print("<a\n             class=\"" + esc_attr(php_implode(" ", classes_)) + "\"\n                href=\"" + esc_url(link_) + "\"\n               data-active-label=\"" + esc_attr(__("Checking for Spam", "akismet")) + "\"\n                data-progress-label-format=\"" + esc_attr(__("(%1$s%)", "akismet")) + "\"\n             data-success-url=\"" + esc_attr(remove_query_arg(Array("akismet_recheck", "akismet_recheck_error"), add_query_arg(Array({"akismet_recheck_complete": 1, "recheck_count": urlencode("__recheck_count__"), "spam_count": urlencode("__spam_count__")})))) + "\"\n             data-failure-url=\"" + esc_attr(remove_query_arg(Array("akismet_recheck", "akismet_recheck_complete"), add_query_arg(Array({"akismet_recheck_error": 1})))) + "\"\n             data-pending-comment-count=\"" + esc_attr(comments_count_.moderated) + "\"\n                data-nonce=\"" + esc_attr(wp_create_nonce("akismet_check_for_spam")) + "\"\n                >")
        php_print("<span class=\"akismet-label\">" + esc_html__("Check for Spam", "akismet") + "</span>")
        php_print("<span class=\"checkforspam-progress\"></span>")
        php_print("</a>")
        php_print("<span class=\"checkforspam-spinner\"></span>")
    # end def check_for_spam_button
    @classmethod
    def recheck_queue(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        Akismet.fix_scheduled_recheck()
        if (not (php_isset(lambda : PHP_REQUEST["recheckqueue"])) or (php_isset(lambda : PHP_REQUEST["action"])) and "akismet_recheck_queue" == PHP_REQUEST["action"]):
            return
        # end if
        if (not wp_verify_nonce(PHP_POST["nonce"], "akismet_check_for_spam")):
            wp_send_json(Array({"error": __("You don't have permission to do that.")}))
            return
        # end if
        result_counts_ = self.recheck_queue_portion(0 if php_empty(lambda : PHP_POST["offset"]) else PHP_POST["offset"], 100 if php_empty(lambda : PHP_POST["limit"]) else PHP_POST["limit"])
        if php_defined("DOING_AJAX") and DOING_AJAX:
            wp_send_json(Array({"counts": result_counts_}))
        else:
            redirect_to_ = PHP_SERVER["HTTP_REFERER"] if (php_isset(lambda : PHP_SERVER["HTTP_REFERER"])) else admin_url("edit-comments.php")
            wp_safe_redirect(redirect_to_)
            php_exit(0)
        # end if
    # end def recheck_queue
    @classmethod
    def recheck_queue_portion(self, start_=0, limit_=100):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        paginate_ = ""
        if limit_ <= 0:
            limit_ = 100
        # end if
        if start_ < 0:
            start_ = 0
        # end if
        moderation_ = wpdb_.get_col(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = '0' LIMIT %d OFFSET %d"), limit_, start_))
        result_counts_ = Array({"processed": php_count(moderation_), "spam": 0, "ham": 0, "error": 0})
        for comment_id_ in moderation_:
            api_response_ = Akismet.recheck_comment(comment_id_, "recheck_queue")
            if "true" == api_response_:
                result_counts_["spam"] += 1
            elif "false" == api_response_:
                result_counts_["ham"] += 1
            else:
                result_counts_["error"] += 1
            # end if
        # end for
        return result_counts_
    # end def recheck_queue_portion
    #// Adds an 'x' link next to author URLs, clicking will remove the author URL and show an undo link
    @classmethod
    def remove_comment_author_url(self):
        
        
        if (not php_empty(lambda : PHP_POST["id"])) and check_admin_referer("comment_author_url_nonce"):
            comment_id_ = php_intval(PHP_POST["id"])
            comment_ = get_comment(comment_id_, ARRAY_A)
            if comment_ and current_user_can("edit_comment", comment_["comment_ID"]):
                comment_["comment_author_url"] = ""
                do_action("comment_remove_author_url")
                php_print(wp_update_comment(comment_))
                php_exit(0)
            # end if
        # end if
    # end def remove_comment_author_url
    @classmethod
    def add_comment_author_url(self):
        
        
        if (not php_empty(lambda : PHP_POST["id"])) and (not php_empty(lambda : PHP_POST["url"])) and check_admin_referer("comment_author_url_nonce"):
            comment_id_ = php_intval(PHP_POST["id"])
            comment_ = get_comment(comment_id_, ARRAY_A)
            if comment_ and current_user_can("edit_comment", comment_["comment_ID"]):
                comment_["comment_author_url"] = esc_url(PHP_POST["url"])
                do_action("comment_add_author_url")
                php_print(wp_update_comment(comment_))
                php_exit(0)
            # end if
        # end if
    # end def add_comment_author_url
    @classmethod
    def comment_row_action(self, a_=None, comment_=None):
        
        
        akismet_result_ = get_comment_meta(comment_.comment_ID, "akismet_result", True)
        akismet_error_ = get_comment_meta(comment_.comment_ID, "akismet_error", True)
        user_result_ = get_comment_meta(comment_.comment_ID, "akismet_user_result", True)
        comment_status_ = wp_get_comment_status(comment_.comment_ID)
        desc_ = None
        if akismet_error_:
            desc_ = __("Awaiting spam check", "akismet")
        elif (not user_result_) or user_result_ == akismet_result_:
            #// Show the original Akismet result if the user hasn't overridden it, or if their decision was the same
            if akismet_result_ == "true" and comment_status_ != "spam" and comment_status_ != "trash":
                desc_ = __("Flagged as spam by Akismet", "akismet")
            elif akismet_result_ == "false" and comment_status_ == "spam":
                desc_ = __("Cleared by Akismet", "akismet")
            # end if
        else:
            who_ = get_comment_meta(comment_.comment_ID, "akismet_user", True)
            if user_result_ == "true":
                desc_ = php_sprintf(__("Flagged as spam by %s", "akismet"), who_)
            else:
                desc_ = php_sprintf(__("Un-spammed by %s", "akismet"), who_)
            # end if
        # end if
        #// add a History item to the hover links, just after Edit
        if akismet_result_:
            b_ = Array()
            for k_,item_ in a_.items():
                b_[k_] = item_
                if k_ == "edit" or k_ == "unspam":
                    b_["history"] = "<a href=\"comment.php?action=editcomment&amp;c=" + comment_.comment_ID + "#akismet-status\" title=\"" + esc_attr__("View comment history", "akismet") + "\"> " + esc_html__("History", "akismet") + "</a>"
                # end if
            # end for
            a_ = b_
        # end if
        if desc_:
            php_print("<span class=\"akismet-status\" commentid=\"" + comment_.comment_ID + "\"><a href=\"comment.php?action=editcomment&amp;c=" + comment_.comment_ID + "#akismet-status\" title=\"" + esc_attr__("View comment history", "akismet") + "\">" + esc_html(desc_) + "</a></span>")
        # end if
        show_user_comments_option_ = get_option("akismet_show_user_comments_approved")
        if show_user_comments_option_ == False:
            #// Default to active if the user hasn't made a decision.
            show_user_comments_option_ = "1"
        # end if
        show_user_comments_ = apply_filters("akismet_show_user_comments_approved", show_user_comments_option_)
        show_user_comments_ = False if show_user_comments_ == "false" else show_user_comments_
        #// option used to be saved as 'false' / 'true'
        if show_user_comments_:
            comment_count_ = Akismet.get_user_comments_approved(comment_.user_id, comment_.comment_author_email, comment_.comment_author, comment_.comment_author_url)
            comment_count_ = php_intval(comment_count_)
            php_print("<span class=\"akismet-user-comment-count\" commentid=\"" + comment_.comment_ID + "\" style=\"display:none;\"><br><span class=\"akismet-user-comment-counts\">" + php_sprintf(esc_html(_n("%s approved", "%s approved", comment_count_, "akismet")), number_format_i18n(comment_count_)) + "</span></span>")
        # end if
        return a_
    # end def comment_row_action
    @classmethod
    def comment_status_meta_box(self, comment_=None):
        
        
        history_ = Akismet.get_comment_history(comment_.comment_ID)
        if history_:
            for row_ in history_:
                time_ = date("D d M Y @ h:i:s a", row_["time"]) + " GMT"
                message_ = ""
                if (not php_empty(lambda : row_["message"])):
                    #// Old versions of Akismet stored the message as a literal string in the commentmeta.
                    #// New versions don't do that for two reasons:
                    #// 1) Save space.
                    #// 2) The message can be translated into the current language of the blog, not stuck
                    #// in the language of the blog when the comment was made.
                    message_ = esc_html(row_["message"])
                # end if
                #// If possible, use a current translation.
                for case in Switch(row_["event"]):
                    if case("recheck-spam"):
                        message_ = esc_html(__("Akismet re-checked and caught this comment as spam.", "akismet"))
                        break
                    # end if
                    if case("check-spam"):
                        message_ = esc_html(__("Akismet caught this comment as spam.", "akismet"))
                        break
                    # end if
                    if case("recheck-ham"):
                        message_ = esc_html(__("Akismet re-checked and cleared this comment.", "akismet"))
                        break
                    # end if
                    if case("check-ham"):
                        message_ = esc_html(__("Akismet cleared this comment.", "akismet"))
                        break
                    # end if
                    if case("wp-blacklisted"):
                        message_ = php_sprintf(esc_html(__("Comment was caught by %s.", "akismet")), "<code>wp_blacklist_check</code>")
                        break
                    # end if
                    if case("report-spam"):
                        if (php_isset(lambda : row_["user"])):
                            message_ = esc_html(php_sprintf(__("%s reported this comment as spam.", "akismet"), row_["user"]))
                        else:
                            if (not message_):
                                message_ = esc_html(__("This comment was reported as spam.", "akismet"))
                            # end if
                        # end if
                        break
                    # end if
                    if case("report-ham"):
                        if (php_isset(lambda : row_["user"])):
                            message_ = esc_html(php_sprintf(__("%s reported this comment as not spam.", "akismet"), row_["user"]))
                        else:
                            if (not message_):
                                message_ = esc_html(__("This comment was reported as not spam.", "akismet"))
                            # end if
                        # end if
                        break
                    # end if
                    if case("cron-retry-spam"):
                        message_ = esc_html(__("Akismet caught this comment as spam during an automatic retry.", "akismet"))
                        break
                    # end if
                    if case("cron-retry-ham"):
                        message_ = esc_html(__("Akismet cleared this comment during an automatic retry.", "akismet"))
                        break
                    # end if
                    if case("check-error"):
                        if (php_isset(lambda : row_["meta"]) and php_isset(lambda : row_["meta"]["response"])):
                            message_ = php_sprintf(esc_html(__("Akismet was unable to check this comment (response: %s) but will automatically retry later.", "akismet")), "<code>" + esc_html(row_["meta"]["response"]) + "</code>")
                        else:
                            message_ = esc_html(__("Akismet was unable to check this comment but will automatically retry later.", "akismet"))
                        # end if
                        break
                    # end if
                    if case("recheck-error"):
                        if (php_isset(lambda : row_["meta"]) and php_isset(lambda : row_["meta"]["response"])):
                            message_ = php_sprintf(esc_html(__("Akismet was unable to recheck this comment (response: %s).", "akismet")), "<code>" + esc_html(row_["meta"]["response"]) + "</code>")
                        else:
                            message_ = esc_html(__("Akismet was unable to recheck this comment.", "akismet"))
                        # end if
                        break
                    # end if
                    if case():
                        if php_preg_match("/^status-changed/", row_["event"]):
                            #// Half of these used to be saved without the dash after 'status-changed'.
                            #// See https://plugins.trac.wordpress.org/changeset/1150658/akismet/trunk
                            new_status_ = php_preg_replace("/^status-changed-?/", "", row_["event"])
                            message_ = php_sprintf(esc_html(__("Comment status was changed to %s", "akismet")), "<code>" + esc_html(new_status_) + "</code>")
                        else:
                            if php_preg_match("/^status-/", row_["event"]):
                                new_status_ = php_preg_replace("/^status-/", "", row_["event"])
                                if (php_isset(lambda : row_["user"])):
                                    message_ = php_sprintf(esc_html(__("%1$s changed the comment status to %2$s.", "akismet")), row_["user"], "<code>" + esc_html(new_status_) + "</code>")
                                # end if
                            # end if
                        # end if
                        break
                    # end if
                # end for
                if (not php_empty(lambda : message_)):
                    php_print("<p>")
                    php_print("<span style=\"color: #999;\" alt=\"" + time_ + "\" title=\"" + time_ + "\">" + php_sprintf(esc_html__("%s ago", "akismet"), human_time_diff(row_["time"])) + "</span>")
                    php_print(" - ")
                    php_print(message_)
                    #// esc_html() is done above so that we can use HTML in some messages.
                    php_print("</p>")
                # end if
            # end for
        else:
            php_print("<p>")
            php_print(esc_html(__("No comment history.", "akismet")))
            php_print("</p>")
        # end if
    # end def comment_status_meta_box
    @classmethod
    def plugin_action_links(self, links_=None, file_=None):
        
        
        if file_ == plugin_basename(plugin_dir_url(__FILE__) + "/akismet.php"):
            links_[-1] = "<a href=\"" + esc_url(self.get_page_url()) + "\">" + esc_html__("Settings", "akismet") + "</a>"
        # end if
        return links_
    # end def plugin_action_links
    #// Total spam in queue
    #// get_option( 'akismet_spam_count' ) is the total caught ever
    @classmethod
    def get_spam_count(self, type_=None):
        if type_ is None:
            type_ = False
        # end if
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not type_):
            #// total
            count_ = wp_cache_get("akismet_spam_count", "widget")
            if False == count_:
                count_ = wp_count_comments()
                count_ = count_.spam
                wp_cache_set("akismet_spam_count", count_, "widget", 3600)
            # end if
            return count_
        elif "comments" == type_ or "comment" == type_:
            #// comments
            type_ = ""
        # end if
        return php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(comment_ID) FROM ") + str(wpdb_.comments) + str(" WHERE comment_approved = 'spam' AND comment_type = %s"), type_)))
    # end def get_spam_count
    #// Check connectivity between the WordPress blog and Akismet's servers.
    #// Returns an associative array of server IP addresses, where the key is the IP address, and value is true (available) or false (unable to connect).
    @classmethod
    def check_server_ip_connectivity(self):
        
        
        servers_ = ips_ = Array()
        #// Some web hosts may disable this function
        if php_function_exists("gethostbynamel"):
            ips_ = gethostbynamel("rest.akismet.com")
            if ips_ and php_is_array(ips_) and php_count(ips_):
                api_key_ = Akismet.get_api_key()
                for ip_ in ips_:
                    response_ = Akismet.verify_key(api_key_, ip_)
                    #// even if the key is invalid, at least we know we have connectivity
                    if response_ == "valid" or response_ == "invalid":
                        servers_[ip_] = "connected"
                    else:
                        servers_[ip_] = response_ if response_ else "unable to connect"
                    # end if
                # end for
            # end if
        # end if
        return servers_
    # end def check_server_ip_connectivity
    #// Simpler connectivity check
    @classmethod
    def check_server_connectivity(self, cache_timeout_=86400):
        
        
        debug_ = Array()
        debug_["PHP_VERSION"] = PHP_VERSION
        debug_["WORDPRESS_VERSION"] = PHP_GLOBALS["wp_version"]
        debug_["AKISMET_VERSION"] = AKISMET_VERSION
        debug_["AKISMET__PLUGIN_DIR"] = AKISMET__PLUGIN_DIR
        debug_["SITE_URL"] = site_url()
        debug_["HOME_URL"] = home_url()
        servers_ = get_option("akismet_available_servers")
        if time() - get_option("akismet_connectivity_time") < cache_timeout_ and servers_ != False:
            servers_ = self.check_server_ip_connectivity()
            update_option("akismet_available_servers", servers_)
            update_option("akismet_connectivity_time", time())
        # end if
        if wp_http_supports(Array("ssl")):
            response_ = wp_remote_get("https://rest.akismet.com/1.1/test")
        else:
            response_ = wp_remote_get("http://rest.akismet.com/1.1/test")
        # end if
        debug_["gethostbynamel"] = "exists" if php_function_exists("gethostbynamel") else "not here"
        debug_["Servers"] = servers_
        debug_["Test Connection"] = response_
        Akismet.log(debug_)
        if response_ and "connected" == wp_remote_retrieve_body(response_):
            return True
        # end if
        return False
    # end def check_server_connectivity
    #// Check the server connectivity and store the available servers in an option.
    @classmethod
    def get_server_connectivity(self, cache_timeout_=86400):
        
        
        return self.check_server_connectivity(cache_timeout_)
    # end def get_server_connectivity
    #// 
    #// Find out whether any comments in the Pending queue have not yet been checked by Akismet.
    #// 
    #// @return bool
    #//
    @classmethod
    def are_any_comments_waiting_to_be_checked(self):
        
        
        return (not (not get_comments(Array({"status": "hold", "meta_key": "akismet_error", "number": 1}))))
    # end def are_any_comments_waiting_to_be_checked
    @classmethod
    def get_page_url(self, page_="config"):
        
        
        args_ = Array({"page": "akismet-key-config"})
        if page_ == "stats":
            args_ = Array({"page": "akismet-key-config", "view": "stats"})
        elif page_ == "delete_key":
            args_ = Array({"page": "akismet-key-config", "view": "start", "action": "delete-key", "_wpnonce": wp_create_nonce(self.NONCE)})
        # end if
        url_ = add_query_arg(args_, admin_url("admin.php") if php_class_exists("Jetpack") else admin_url("options-general.php"))
        return url_
    # end def get_page_url
    @classmethod
    def get_akismet_user(self, api_key_=None):
        
        
        akismet_user_ = False
        subscription_verification_ = Akismet.http_post(Akismet.build_query(Array({"key": api_key_, "blog": get_option("home")})), "get-subscription")
        if (not php_empty(lambda : subscription_verification_[1])):
            if "invalid" != subscription_verification_[1]:
                akismet_user_ = php_json_decode(subscription_verification_[1])
            # end if
        # end if
        return akismet_user_
    # end def get_akismet_user
    @classmethod
    def get_stats(self, api_key_=None):
        
        
        stat_totals_ = Array()
        for interval_ in Array("6-months", "all"):
            response_ = Akismet.http_post(Akismet.build_query(Array({"blog": get_option("home"), "key": api_key_, "from": interval_})), "get-stats")
            if (not php_empty(lambda : response_[1])):
                stat_totals_[interval_] = php_json_decode(response_[1])
            # end if
        # end for
        return stat_totals_
    # end def get_stats
    @classmethod
    def verify_wpcom_key(self, api_key_=None, user_id_=None, extra_=None):
        if extra_ is None:
            extra_ = Array()
        # end if
        
        akismet_account_ = Akismet.http_post(Akismet.build_query(php_array_merge(Array({"user_id": user_id_, "api_key": api_key_, "get_account_type": "true"}), extra_)), "verify-wpcom-key")
        if (not php_empty(lambda : akismet_account_[1])):
            akismet_account_ = php_json_decode(akismet_account_[1])
        # end if
        Akismet.log(php_compact("akismet_account_"))
        return akismet_account_
    # end def verify_wpcom_key
    @classmethod
    def connect_jetpack_user(self):
        
        
        jetpack_user_ = self.get_jetpack_user()
        if jetpack_user_:
            if (php_isset(lambda : jetpack_user_["user_id"])) and (php_isset(lambda : jetpack_user_["api_key"])):
                akismet_user_ = self.verify_wpcom_key(jetpack_user_["api_key"], jetpack_user_["user_id"], Array({"action": "connect_jetpack_user"}))
                if php_is_object(akismet_user_):
                    self.save_key(akismet_user_.api_key)
                    return php_in_array(akismet_user_.status, Array("active", "active-dunning", "no-sub"))
                # end if
            # end if
        # end if
        return False
    # end def connect_jetpack_user
    @classmethod
    def display_alert(self):
        
        
        Akismet.view("notice", Array({"type": "alert", "code": php_int(get_option("akismet_alert_code")), "msg": get_option("akismet_alert_msg")}))
    # end def display_alert
    @classmethod
    def display_privacy_notice_control_warning(self):
        
        
        if (not current_user_can("manage_options")):
            return
        # end if
        Akismet.view("notice", Array({"type": "privacy"}))
    # end def display_privacy_notice_control_warning
    @classmethod
    def display_spam_check_warning(self):
        
        
        Akismet.fix_scheduled_recheck()
        if wp_next_scheduled("akismet_schedule_cron_recheck") > time() and self.are_any_comments_waiting_to_be_checked():
            link_text_ = apply_filters("akismet_spam_check_warning_link_text", php_sprintf(__("Please check your <a href=\"%s\">Akismet configuration</a> and contact your web host if problems persist.", "akismet"), esc_url(self.get_page_url())))
            Akismet.view("notice", Array({"type": "spam-check", "link_text": link_text_}))
        # end if
    # end def display_spam_check_warning
    @classmethod
    def display_api_key_warning(self):
        
        
        Akismet.view("notice", Array({"type": "plugin"}))
    # end def display_api_key_warning
    @classmethod
    def display_page(self):
        
        
        if (not Akismet.get_api_key()) or (php_isset(lambda : PHP_REQUEST["view"])) and PHP_REQUEST["view"] == "start":
            self.display_start_page()
        elif (php_isset(lambda : PHP_REQUEST["view"])) and PHP_REQUEST["view"] == "stats":
            self.display_stats_page()
        else:
            self.display_configuration_page()
        # end if
    # end def display_page
    @classmethod
    def display_start_page(self):
        
        
        if (php_isset(lambda : PHP_REQUEST["action"])):
            if PHP_REQUEST["action"] == "delete-key":
                if (php_isset(lambda : PHP_REQUEST["_wpnonce"])) and wp_verify_nonce(PHP_REQUEST["_wpnonce"], self.NONCE):
                    delete_option("wordpress_api_key")
                # end if
            # end if
        # end if
        api_key_ = Akismet.get_api_key() and php_empty(lambda : self.notices["status"]) or "existing-key-invalid" != self.notices["status"]
        if api_key_:
            self.display_configuration_page()
            return
        # end if
        #// the user can choose to auto connect their API key by clicking a button on the akismet done page
        #// if jetpack, get verified api key by using connected wpcom user id
        #// if no jetpack, get verified api key by using an akismet token
        akismet_user_ = False
        if (php_isset(lambda : PHP_REQUEST["token"])) and php_preg_match("/^(\\d+)-[0-9a-f]{20}$/", PHP_REQUEST["token"]):
            akismet_user_ = self.verify_wpcom_key("", "", Array({"token": PHP_REQUEST["token"]}))
        elif self.get_jetpack_user():
            jetpack_user_ = self.get_jetpack_user()
            akismet_user_ = self.verify_wpcom_key(jetpack_user_["api_key"], jetpack_user_["user_id"])
        # end if
        if (php_isset(lambda : PHP_REQUEST["action"])):
            if PHP_REQUEST["action"] == "save-key":
                if php_is_object(akismet_user_):
                    self.save_key(akismet_user_.api_key)
                    self.display_configuration_page()
                    return
                # end if
            # end if
        # end if
        Akismet.view("start", php_compact("akismet_user_"))
        pass
    # end def display_start_page
    @classmethod
    def display_stats_page(self):
        
        
        Akismet.view("stats")
    # end def display_stats_page
    @classmethod
    def display_configuration_page(self):
        
        
        api_key_ = Akismet.get_api_key()
        akismet_user_ = self.get_akismet_user(api_key_)
        if (not akismet_user_):
            #// This could happen if the user's key became invalid after it was previously valid and successfully set up.
            self.notices["status"] = "existing-key-invalid"
            self.display_start_page()
            return
        # end if
        stat_totals_ = self.get_stats(api_key_)
        #// If unset, create the new strictness option using the old discard option to determine its default.
        #// If the old option wasn't set, default to discarding the blatant spam.
        if get_option("akismet_strictness") == False:
            add_option("akismet_strictness", "0" if get_option("akismet_discard_month") == "false" else "1")
        # end if
        #// Sync the local "Total spam blocked" count with the authoritative count from the server.
        if (php_isset(lambda : stat_totals_["all"]) and php_isset(lambda : stat_totals_["all"].spam)):
            update_option("akismet_spam_count", stat_totals_["all"].spam)
        # end if
        notices_ = Array()
        if php_empty(lambda : self.notices):
            if (not php_empty(lambda : stat_totals_["all"])) and (php_isset(lambda : stat_totals_["all"].time_saved)) and akismet_user_.status == "active" and akismet_user_.account_type == "free-api-key":
                time_saved_ = False
                if stat_totals_["all"].time_saved > 1800:
                    total_in_minutes_ = round(stat_totals_["all"].time_saved / 60)
                    total_in_hours_ = round(total_in_minutes_ / 60)
                    total_in_days_ = round(total_in_hours_ / 8)
                    cleaning_up_ = __("Cleaning up spam takes time.", "akismet")
                    if total_in_days_ > 1:
                        time_saved_ = cleaning_up_ + " " + php_sprintf(_n("Akismet has saved you %s day!", "Akismet has saved you %s days!", total_in_days_, "akismet"), number_format_i18n(total_in_days_))
                    elif total_in_hours_ > 1:
                        time_saved_ = cleaning_up_ + " " + php_sprintf(_n("Akismet has saved you %d hour!", "Akismet has saved you %d hours!", total_in_hours_, "akismet"), total_in_hours_)
                    elif total_in_minutes_ >= 30:
                        time_saved_ = cleaning_up_ + " " + php_sprintf(_n("Akismet has saved you %d minute!", "Akismet has saved you %d minutes!", total_in_minutes_, "akismet"), total_in_minutes_)
                    # end if
                # end if
                notices_[-1] = Array({"type": "active-notice", "time_saved": time_saved_})
            # end if
            if (not php_empty(lambda : akismet_user_.limit_reached)) and php_in_array(akismet_user_.limit_reached, Array("yellow", "red")):
                notices_[-1] = Array({"type": "limit-reached", "level": akismet_user_.limit_reached})
            # end if
        # end if
        if (not (php_isset(lambda : self.notices["status"]))) and php_in_array(akismet_user_.status, Array("cancelled", "suspended", "missing", "no-sub")):
            notices_[-1] = Array({"type": akismet_user_.status})
        # end if
        if False == get_option("akismet_comment_form_privacy_notice"):
            notices_[-1] = Array({"type": "privacy"})
        # end if
        #// 
        #// To see all variants when testing.
        #// $notices[] = array( 'type' => 'active-notice', 'time_saved' => 'Cleaning up spam takes time. Akismet has saved you 1 minute!' );
        #// $notices[] = array( 'type' => 'plugin' );
        #// $notices[] = array( 'type' => 'spam-check', 'link_text' => 'Link text.' );
        #// $notices[] = array( 'type' => 'notice', 'notice_header' => 'This is the notice header.', 'notice_text' => 'This is the notice text.' );
        #// $notices[] = array( 'type' => 'missing-functions' );
        #// $notices[] = array( 'type' => 'servers-be-down' );
        #// $notices[] = array( 'type' => 'active-dunning' );
        #// $notices[] = array( 'type' => 'cancelled' );
        #// $notices[] = array( 'type' => 'suspended' );
        #// $notices[] = array( 'type' => 'missing' );
        #// $notices[] = array( 'type' => 'no-sub' );
        #// $notices[] = array( 'type' => 'new-key-valid' );
        #// $notices[] = array( 'type' => 'new-key-invalid' );
        #// $notices[] = array( 'type' => 'existing-key-invalid' );
        #// $notices[] = array( 'type' => 'new-key-failed' );
        #// $notices[] = array( 'type' => 'limit-reached', 'level' => 'yellow' );
        #// $notices[] = array( 'type' => 'limit-reached', 'level' => 'red' );
        #//
        Akismet.log(php_compact("stat_totals_", "akismet_user_"))
        Akismet.view("config", php_compact("api_key_", "akismet_user_", "stat_totals_", "notices_"))
    # end def display_configuration_page
    @classmethod
    def display_notice(self):
        
        
        global hook_suffix_
        php_check_if_defined("hook_suffix_")
        if php_in_array(hook_suffix_, Array("jetpack_page_akismet-key-config", "settings_page_akismet-key-config")):
            #// This page manages the notices and puts them inline where they make sense.
            return
        # end if
        if php_in_array(hook_suffix_, Array("edit-comments.php")) and php_int(get_option("akismet_alert_code")) > 0:
            Akismet.verify_key(Akismet.get_api_key())
            #// verify that the key is still in alert state
            if get_option("akismet_alert_code") > 0:
                self.display_alert()
            # end if
        elif hook_suffix_ == "plugins.php" and (not Akismet.get_api_key()):
            self.display_api_key_warning()
        elif hook_suffix_ == "edit-comments.php" and wp_next_scheduled("akismet_schedule_cron_recheck"):
            self.display_spam_check_warning()
        # end if
        if (php_isset(lambda : PHP_REQUEST["akismet_recheck_complete"])):
            recheck_count_ = php_int(PHP_REQUEST["recheck_count"])
            spam_count_ = php_int(PHP_REQUEST["spam_count"])
            if recheck_count_ == 0:
                message_ = __("There were no comments to check. Akismet will only check comments awaiting moderation.", "akismet")
            else:
                message_ = php_sprintf(_n("Akismet checked %s comment.", "Akismet checked %s comments.", recheck_count_, "akismet"), number_format(recheck_count_))
                message_ += " "
                if spam_count_ == 0:
                    message_ += __("No comments were caught as spam.", "akismet")
                else:
                    message_ += php_sprintf(_n("%s comment was caught as spam.", "%s comments were caught as spam.", spam_count_, "akismet"), number_format(spam_count_))
                # end if
            # end if
            php_print("<div class=\"notice notice-success\"><p>" + esc_html(message_) + "</p></div>")
        else:
            if (php_isset(lambda : PHP_REQUEST["akismet_recheck_error"])):
                php_print("<div class=\"notice notice-error\"><p>" + esc_html(__("Akismet could not recheck your comments for spam.", "akismet")) + "</p></div>")
            # end if
        # end if
        akismet_comment_form_privacy_notice_option_ = get_option("akismet_comment_form_privacy_notice")
        if (not php_in_array(akismet_comment_form_privacy_notice_option_, Array("hide", "display"))):
            api_key_ = Akismet.get_api_key()
            if (not php_empty(lambda : api_key_)):
                self.display_privacy_notice_control_warning()
            # end if
        # end if
    # end def display_notice
    @classmethod
    def display_status(self):
        
        
        if (not self.get_server_connectivity()):
            Akismet.view("notice", Array({"type": "servers-be-down"}))
        else:
            if (not php_empty(lambda : self.notices)):
                for index_,type_ in self.notices.items():
                    if php_is_object(type_):
                        notice_header_ = notice_text_
                        if property_exists(type_, "notice_header"):
                            notice_header_ = wp_kses(type_.notice_header, self.allowed)
                        # end if
                        if property_exists(type_, "notice_text"):
                            notice_text_ = wp_kses(type_.notice_text, self.allowed)
                        # end if
                        if property_exists(type_, "status"):
                            type_ = wp_kses(type_.status, self.allowed)
                            Akismet.view("notice", php_compact("type_", "notice_header_", "notice_text_"))
                            self.notices[index_] = None
                        # end if
                    else:
                        Akismet.view("notice", php_compact("type_"))
                        self.notices[index_] = None
                    # end if
                # end for
            # end if
        # end if
    # end def display_status
    def get_jetpack_user(self):
        
        
        if (not php_class_exists("Jetpack")):
            return False
        # end if
        if php_defined("JETPACK__VERSION") and php_version_compare(JETPACK__VERSION, "7.7", "<"):
            #// For version of Jetpack prior to 7.7.
            Jetpack.load_xml_rpc_client()
        # end if
        xml_ = php_new_class("Jetpack_IXR_ClientMulticall", lambda : Jetpack_IXR_ClientMulticall(Array({"user_id": get_current_user_id()})))
        xml_.addcall("wpcom.getUserID")
        xml_.addcall("akismet.getAPIKey")
        xml_.query()
        Akismet.log(php_compact("xml_"))
        if (not xml_.iserror()):
            responses_ = xml_.getresponse()
            if php_count(responses_) > 1:
                #// Due to a quirk in how Jetpack does multi-calls, the response order
                #// can't be trusted to match the call order. It's a good thing our
                #// return values can be mostly differentiated from each other.
                first_response_value_ = php_array_shift(responses_[0])
                second_response_value_ = php_array_shift(responses_[1])
                #// If WPCOM ever reaches 100 billion users, this will fail. :-)
                if php_preg_match("/^[a-f0-9]{12}$/i", first_response_value_):
                    api_key_ = first_response_value_
                    user_id_ = php_int(second_response_value_)
                else:
                    api_key_ = second_response_value_
                    user_id_ = php_int(first_response_value_)
                # end if
                return php_compact("api_key_", "user_id_")
            # end if
        # end if
        return False
    # end def get_jetpack_user
    #// 
    #// Some commentmeta isn't useful in an export file. Suppress it (when supported).
    #// 
    #// @param bool $exclude
    #// @param string $key The meta key
    #// @param object $meta The meta object
    #// @return bool Whether to exclude this meta entry from the export.
    #//
    @classmethod
    def exclude_commentmeta_from_export(self, exclude_=None, key_=None, meta_=None):
        
        
        if php_in_array(key_, Array("akismet_as_submitted", "akismet_rechecking", "akismet_delayed_moderation_email")):
            return True
        # end if
        return exclude_
    # end def exclude_commentmeta_from_export
    #// 
    #// When Akismet is active, remove the "Activate Akismet" step from the plugin description.
    #//
    @classmethod
    def modify_plugin_description(self, all_plugins_=None):
        
        
        if (php_isset(lambda : all_plugins_["akismet/akismet.php"])):
            if Akismet.get_api_key():
                all_plugins_["akismet/akismet.php"]["Description"] = __("Used by millions, Akismet is quite possibly the best way in the world to <strong>protect your blog from spam</strong>. Your site is fully configured and being protected, even while you sleep.", "akismet")
            else:
                all_plugins_["akismet/akismet.php"]["Description"] = __("Used by millions, Akismet is quite possibly the best way in the world to <strong>protect your blog from spam</strong>. It keeps your site protected even while you sleep. To get started, just go to <a href=\"admin.php?page=akismet-key-config\">your Akismet Settings page</a> to set up your API key.", "akismet")
            # end if
        # end if
        return all_plugins_
    # end def modify_plugin_description
    def set_form_privacy_notice_option(self, state_=None):
        
        
        if php_in_array(state_, Array("display", "hide")):
            update_option("akismet_comment_form_privacy_notice", state_)
        # end if
    # end def set_form_privacy_notice_option
    @classmethod
    def jetpack_comment_form_privacy_notice_url(self, url_=None):
        
        
        return php_str_replace("options-general.php", "admin.php", url_)
    # end def jetpack_comment_form_privacy_notice_url
    @classmethod
    def register_personal_data_eraser(self, erasers_=None):
        
        
        erasers_["akismet"] = Array({"eraser_friendly_name": __("Akismet", "akismet"), "callback": Array("Akismet_Admin", "erase_personal_data")})
        return erasers_
    # end def register_personal_data_eraser
    #// 
    #// When a user requests that their personal data be removed, Akismet has a duty to discard
    #// any personal data we store outside of the comment itself. Right now, that is limited
    #// to the copy of the comment we store in the akismet_as_submitted commentmeta.
    #// 
    #// FWIW, this information would be automatically deleted after 15 days.
    #// 
    #// @param $email_address string The email address of the user who has requested erasure.
    #// @param $page int This function can (and will) be called multiple times to prevent timeouts,
    #// so this argument is used for pagination.
    #// @return array
    #// @see https://developer.wordpress.org/plugins/privacy/adding-the-personal-data-eraser-to-your-plugin
    #//
    @classmethod
    def erase_personal_data(self, email_address_=None, page_=1):
        
        
        items_removed_ = False
        number_ = 50
        page_ = php_int(page_)
        comments_ = get_comments(Array({"author_email": email_address_, "number": number_, "paged": page_, "order_by": "comment_ID", "order": "ASC"}))
        for comment_ in comments_:
            comment_as_submitted_ = get_comment_meta(comment_.comment_ID, "akismet_as_submitted", True)
            if comment_as_submitted_:
                delete_comment_meta(comment_.comment_ID, "akismet_as_submitted")
                items_removed_ = True
            # end if
        # end for
        #// Tell core if we have more comments to work on still
        done_ = php_count(comments_) < number_
        return Array({"items_removed": items_removed_, "items_retained": False, "messages": Array(), "done": done_})
    # end def erase_personal_data
# end class Akismet_Admin
