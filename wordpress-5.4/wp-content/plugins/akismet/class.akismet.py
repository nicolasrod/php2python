#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
class Akismet():
    API_HOST = "rest.akismet.com"
    API_PORT = 80
    MAX_DELAY_BEFORE_MODERATION_EMAIL = 86400
    #// One day in seconds
    last_comment = ""
    initiated = False
    prevent_moderation_email_for_these_comments = Array()
    last_comment_result = None
    comment_as_submitted_allowed_keys = Array({"blog": "", "blog_charset": "", "blog_lang": "", "blog_ua": "", "comment_agent": "", "comment_author": "", "comment_author_IP": "", "comment_author_email": "", "comment_author_url": "", "comment_content": "", "comment_date_gmt": "", "comment_tags": "", "comment_type": "", "guid": "", "is_test": "", "permalink": "", "reporter": "", "site_domain": "", "submit_referer": "", "submit_uri": "", "user_ID": "", "user_agent": "", "user_id": "", "user_ip": ""})
    is_rest_api_call = False
    @classmethod
    def init(self):
        
        
        if (not self.initiated):
            self.init_hooks()
        # end if
    # end def init
    #// 
    #// Initializes WordPress hooks
    #//
    def init_hooks(self):
        
        
        self.initiated = True
        add_action("wp_insert_comment", Array("Akismet", "auto_check_update_meta"), 10, 2)
        add_filter("preprocess_comment", Array("Akismet", "auto_check_comment"), 1)
        add_filter("rest_pre_insert_comment", Array("Akismet", "rest_auto_check_comment"), 1)
        add_action("akismet_scheduled_delete", Array("Akismet", "delete_old_comments"))
        add_action("akismet_scheduled_delete", Array("Akismet", "delete_old_comments_meta"))
        add_action("akismet_scheduled_delete", Array("Akismet", "delete_orphaned_commentmeta"))
        add_action("akismet_schedule_cron_recheck", Array("Akismet", "cron_recheck"))
        add_action("comment_form", Array("Akismet", "add_comment_nonce"), 1)
        add_action("admin_head-edit-comments.php", Array("Akismet", "load_form_js"))
        add_action("comment_form", Array("Akismet", "load_form_js"))
        add_action("comment_form", Array("Akismet", "inject_ak_js"))
        add_filter("script_loader_tag", Array("Akismet", "set_form_js_async"), 10, 3)
        add_filter("comment_moderation_recipients", Array("Akismet", "disable_moderation_emails_if_unreachable"), 1000, 2)
        add_filter("pre_comment_approved", Array("Akismet", "last_comment_status"), 10, 2)
        add_action("transition_comment_status", Array("Akismet", "transition_comment_status"), 10, 3)
        #// Run this early in the pingback call, before doing a remote fetch of the source uri
        add_action("xmlrpc_call", Array("Akismet", "pre_check_pingback"))
        #// Jetpack compatibility
        add_filter("jetpack_options_whitelist", Array("Akismet", "add_to_jetpack_options_whitelist"))
        add_action("update_option_wordpress_api_key", Array("Akismet", "updated_option"), 10, 2)
        add_action("add_option_wordpress_api_key", Array("Akismet", "added_option"), 10, 2)
        add_action("comment_form_after", Array("Akismet", "display_comment_form_privacy_notice"))
    # end def init_hooks
    @classmethod
    def get_api_key(self):
        
        
        return apply_filters("akismet_get_api_key", constant("WPCOM_API_KEY") if php_defined("WPCOM_API_KEY") else get_option("wordpress_api_key"))
    # end def get_api_key
    @classmethod
    def check_key_status(self, key_=None, ip_=None):
        if ip_ is None:
            ip_ = None
        # end if
        
        return self.http_post(Akismet.build_query(Array({"key": key_, "blog": get_option("home")})), "verify-key", ip_)
    # end def check_key_status
    @classmethod
    def verify_key(self, key_=None, ip_=None):
        if ip_ is None:
            ip_ = None
        # end if
        
        #// Shortcut for obviously invalid keys.
        if php_strlen(key_) != 12:
            return "invalid"
        # end if
        response_ = self.check_key_status(key_, ip_)
        if response_[1] != "valid" and response_[1] != "invalid":
            return "failed"
        # end if
        return response_[1]
    # end def verify_key
    @classmethod
    def deactivate_key(self, key_=None):
        
        
        response_ = self.http_post(Akismet.build_query(Array({"key": key_, "blog": get_option("home")})), "deactivate")
        if response_[1] != "deactivated":
            return "failed"
        # end if
        return response_[1]
    # end def deactivate_key
    #// 
    #// Add the akismet option to the Jetpack options management whitelist.
    #// 
    #// @param array $options The list of whitelisted option names.
    #// @return array The updated whitelist
    #//
    @classmethod
    def add_to_jetpack_options_whitelist(self, options_=None):
        
        
        options_[-1] = "wordpress_api_key"
        return options_
    # end def add_to_jetpack_options_whitelist
    #// 
    #// When the akismet option is updated, run the registration call.
    #// 
    #// This should only be run when the option is updated from the Jetpack/WP.com
    #// API call, and only if the new key is different than the old key.
    #// 
    #// @param mixed  $old_value   The old option value.
    #// @param mixed  $value       The new option value.
    #//
    @classmethod
    def updated_option(self, old_value_=None, value_=None):
        
        
        #// Not an API call
        if (not php_class_exists("WPCOM_JSON_API_Update_Option_Endpoint")):
            return
        # end if
        #// Only run the registration if the old key is different.
        if old_value_ != value_:
            self.verify_key(value_)
        # end if
    # end def updated_option
    #// 
    #// Treat the creation of an API key the same as updating the API key to a new value.
    #// 
    #// @param mixed  $option_name   Will always be "wordpress_api_key", until something else hooks in here.
    #// @param mixed  $value         The option value.
    #//
    @classmethod
    def added_option(self, option_name_=None, value_=None):
        
        
        if "wordpress_api_key" == option_name_:
            return self.updated_option("", value_)
        # end if
    # end def added_option
    @classmethod
    def rest_auto_check_comment(self, commentdata_=None):
        
        
        self.is_rest_api_call = True
        return self.auto_check_comment(commentdata_)
    # end def rest_auto_check_comment
    @classmethod
    def auto_check_comment(self, commentdata_=None):
        
        
        #// If no key is configured, then there's no point in doing any of this.
        if (not self.get_api_key()):
            return commentdata_
        # end if
        self.last_comment_result = None
        comment_ = commentdata_
        comment_["user_ip"] = self.get_ip_address()
        comment_["user_agent"] = self.get_user_agent()
        comment_["referrer"] = self.get_referer()
        comment_["blog"] = get_option("home")
        comment_["blog_lang"] = get_locale()
        comment_["blog_charset"] = get_option("blog_charset")
        comment_["permalink"] = get_permalink(comment_["comment_post_ID"])
        if (not php_empty(lambda : comment_["user_ID"])):
            comment_["user_role"] = Akismet.get_user_roles(comment_["user_ID"])
        # end if
        #// See filter documentation in init_hooks().
        akismet_nonce_option_ = apply_filters("akismet_comment_nonce", get_option("akismet_comment_nonce"))
        comment_["akismet_comment_nonce"] = "inactive"
        if akismet_nonce_option_ == "true" or akismet_nonce_option_ == "":
            comment_["akismet_comment_nonce"] = "failed"
            if (php_isset(lambda : PHP_POST["akismet_comment_nonce"])) and wp_verify_nonce(PHP_POST["akismet_comment_nonce"], "akismet_comment_nonce_" + comment_["comment_post_ID"]):
                comment_["akismet_comment_nonce"] = "passed"
            # end if
            #// comment reply in wp-admin
            if (php_isset(lambda : PHP_POST["_ajax_nonce-replyto-comment"])) and check_ajax_referer("replyto-comment", "_ajax_nonce-replyto-comment"):
                comment_["akismet_comment_nonce"] = "passed"
            # end if
        # end if
        if self.is_test_mode():
            comment_["is_test"] = "true"
        # end if
        for key_,value_ in PHP_POST.items():
            if php_is_string(value_):
                comment_[str("POST_") + str(key_)] = value_
            # end if
        # end for
        for key_,value_ in PHP_SERVER.items():
            if (not php_is_string(value_)):
                continue
            # end if
            if php_preg_match("/^HTTP_COOKIE/", key_):
                continue
            # end if
            #// Send any potentially useful $_SERVER vars, but avoid sending junk we don't need.
            if php_preg_match("/^(HTTP_|REMOTE_ADDR|REQUEST_URI|DOCUMENT_URI)/", key_):
                comment_[str(key_)] = value_
            # end if
        # end for
        post_ = get_post(comment_["comment_post_ID"])
        if (not php_is_null(post_)):
            #// $post can technically be null, although in the past, it's always been an indicator of another plugin interfering.
            comment_["comment_post_modified_gmt"] = post_.post_modified_gmt
        # end if
        response_ = self.http_post(Akismet.build_query(comment_), "comment-check")
        do_action("akismet_comment_check_response", response_)
        commentdata_["comment_as_submitted"] = php_array_intersect_key(comment_, self.comment_as_submitted_allowed_keys)
        commentdata_["akismet_result"] = response_[1]
        if (php_isset(lambda : response_[0]["x-akismet-pro-tip"])):
            commentdata_["akismet_pro_tip"] = response_[0]["x-akismet-pro-tip"]
        # end if
        if (php_isset(lambda : response_[0]["x-akismet-error"])):
            #// An error occurred that we anticipated (like a suspended key) and want the user to act on.
            #// Send to moderation.
            self.last_comment_result = "0"
        else:
            if "true" == response_[1]:
                #// akismet_spam_count will be incremented later by comment_is_spam()
                self.last_comment_result = "spam"
                discard_ = (php_isset(lambda : commentdata_["akismet_pro_tip"])) and commentdata_["akismet_pro_tip"] == "discard" and self.allow_discard()
                do_action("akismet_spam_caught", discard_)
                if discard_:
                    #// The spam is obvious, so we're bailing out early.
                    #// akismet_result_spam() won't be called so bump the counter here
                    incr_ = apply_filters("akismet_spam_count_incr", 1)
                    if incr_:
                        update_option("akismet_spam_count", get_option("akismet_spam_count") + incr_)
                    # end if
                    if self.is_rest_api_call:
                        return php_new_class("WP_Error", lambda : WP_Error("akismet_rest_comment_discarded", __("Comment discarded.", "akismet")))
                    else:
                        #// Redirect back to the previous page, or failing that, the post permalink, or failing that, the homepage of the blog.
                        redirect_to_ = PHP_SERVER["HTTP_REFERER"] if (php_isset(lambda : PHP_SERVER["HTTP_REFERER"])) else get_permalink(post_) if post_ else home_url()
                        wp_safe_redirect(esc_url_raw(redirect_to_))
                        php_exit(0)
                    # end if
                else:
                    if self.is_rest_api_call:
                        #// The way the REST API structures its calls, we can set the comment_approved value right away.
                        commentdata_["comment_approved"] = "spam"
                    # end if
                # end if
            # end if
        # end if
        #// if the response is neither true nor false, hold the comment for moderation and schedule a recheck
        if "true" != response_[1] and "false" != response_[1]:
            if (not current_user_can("moderate_comments")):
                #// Comment status should be moderated
                self.last_comment_result = "0"
            # end if
            if (not wp_next_scheduled("akismet_schedule_cron_recheck")):
                wp_schedule_single_event(time() + 1200, "akismet_schedule_cron_recheck")
                do_action("akismet_scheduled_recheck", "invalid-response-" + response_[1])
            # end if
            self.prevent_moderation_email_for_these_comments[-1] = commentdata_
        # end if
        #// Delete old comments daily
        if (not wp_next_scheduled("akismet_scheduled_delete")):
            wp_schedule_event(time(), "daily", "akismet_scheduled_delete")
        # end if
        self.set_last_comment(commentdata_)
        self.fix_scheduled_recheck()
        return commentdata_
    # end def auto_check_comment
    @classmethod
    def get_last_comment(self):
        
        
        return self.last_comment
    # end def get_last_comment
    @classmethod
    def set_last_comment(self, comment_=None):
        
        
        if php_is_null(comment_):
            self.last_comment = None
        else:
            #// We filter it here so that it matches the filtered comment data that we'll have to compare against later.
            #// wp_filter_comment expects comment_author_IP
            self.last_comment = wp_filter_comment(php_array_merge(Array({"comment_author_IP": self.get_ip_address()}), comment_))
        # end if
    # end def set_last_comment
    #// this fires on wp_insert_comment.  we can't update comment_meta when auto_check_comment() runs
    #// because we don't know the comment ID at that point.
    @classmethod
    def auto_check_update_meta(self, id_=None, comment_=None):
        
        
        #// wp_insert_comment() might be called in other contexts, so make sure this is the same comment
        #// as was checked by auto_check_comment
        if php_is_object(comment_) and (not php_empty(lambda : self.last_comment)) and php_is_array(self.last_comment):
            if self.matches_last_comment(comment_):
                load_plugin_textdomain("akismet")
                #// normal result: true or false
                if self.last_comment["akismet_result"] == "true":
                    update_comment_meta(comment_.comment_ID, "akismet_result", "true")
                    self.update_comment_history(comment_.comment_ID, "", "check-spam")
                    if comment_.comment_approved != "spam":
                        self.update_comment_history(comment_.comment_ID, "", "status-changed-" + comment_.comment_approved)
                    # end if
                elif self.last_comment["akismet_result"] == "false":
                    update_comment_meta(comment_.comment_ID, "akismet_result", "false")
                    self.update_comment_history(comment_.comment_ID, "", "check-ham")
                    #// Status could be spam or trash, depending on the WP version and whether this change applies:
                    #// https://core.trac.wordpress.org/changeset/34726
                    if comment_.comment_approved == "spam" or comment_.comment_approved == "trash":
                        if wp_blacklist_check(comment_.comment_author, comment_.comment_author_email, comment_.comment_author_url, comment_.comment_content, comment_.comment_author_IP, comment_.comment_agent):
                            self.update_comment_history(comment_.comment_ID, "", "wp-blacklisted")
                        else:
                            self.update_comment_history(comment_.comment_ID, "", "status-changed-" + comment_.comment_approved)
                        # end if
                    # end if
                else:
                    update_comment_meta(comment_.comment_ID, "akismet_error", time())
                    self.update_comment_history(comment_.comment_ID, "", "check-error", Array({"response": php_substr(self.last_comment["akismet_result"], 0, 50)}))
                # end if
                #// record the complete original data as submitted for checking
                if (php_isset(lambda : self.last_comment["comment_as_submitted"])):
                    update_comment_meta(comment_.comment_ID, "akismet_as_submitted", self.last_comment["comment_as_submitted"])
                # end if
                if (php_isset(lambda : self.last_comment["akismet_pro_tip"])):
                    update_comment_meta(comment_.comment_ID, "akismet_pro_tip", self.last_comment["akismet_pro_tip"])
                # end if
            # end if
        # end if
    # end def auto_check_update_meta
    @classmethod
    def delete_old_comments(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// 
        #// Determines how many comments will be deleted in each batch.
        #// 
        #// @param int The default, as defined by AKISMET_DELETE_LIMIT.
        #//
        delete_limit_ = apply_filters("akismet_delete_comment_limit", AKISMET_DELETE_LIMIT if php_defined("AKISMET_DELETE_LIMIT") else 10000)
        delete_limit_ = php_max(1, php_intval(delete_limit_))
        #// 
        #// Determines how many days a comment will be left in the Spam queue before being deleted.
        #// 
        #// @param int The default number of days.
        #//
        delete_interval_ = apply_filters("akismet_delete_comment_interval", 15)
        delete_interval_ = php_max(1, php_intval(delete_interval_))
        while True:
            comment_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT comment_id FROM ") + str(wpdb_.comments) + str(" WHERE DATE_SUB(NOW(), INTERVAL %d DAY) > comment_date_gmt AND comment_approved = 'spam' LIMIT %d"), delete_interval_, delete_limit_))
            if not (comment_ids_):
                break
            # end if
            if php_empty(lambda : comment_ids_):
                return
            # end if
            wpdb_.queries = Array()
            for comment_id_ in comment_ids_:
                do_action("delete_comment", comment_id_)
                do_action("akismet_batch_delete_count", inspect.currentframe().f_code.co_name)
            # end for
            #// Prepared as strings since comment_id is an unsigned BIGINT, and using %d will constrain the value to the maximum signed BIGINT.
            format_string_ = php_implode(", ", array_fill(0, php_count(comment_ids_), "%s"))
            wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.comments) + str(" WHERE comment_id IN ( ") + format_string_ + " )", comment_ids_))
            wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.commentmeta) + str(" WHERE comment_id IN ( ") + format_string_ + " )", comment_ids_))
            clean_comment_cache(comment_ids_)
            do_action("akismet_delete_comment_batch", php_count(comment_ids_))
        # end while
        if apply_filters("akismet_optimize_table", mt_rand(1, 5000) == 11, wpdb_.comments):
            #// lucky number
            wpdb_.query(str("OPTIMIZE TABLE ") + str(wpdb_.comments))
        # end if
    # end def delete_old_comments
    @classmethod
    def delete_old_comments_meta(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        interval_ = apply_filters("akismet_delete_commentmeta_interval", 15)
        #// # enforce a minimum of 1 day
        interval_ = absint(interval_)
        if interval_ < 1:
            interval_ = 1
        # end if
        #// akismet_as_submitted meta values are large, so expire them
        #// after $interval days regardless of the comment status
        while True:
            comment_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT m.comment_id FROM ") + str(wpdb_.commentmeta) + str(" as m INNER JOIN ") + str(wpdb_.comments) + str(" as c USING(comment_id) WHERE m.meta_key = 'akismet_as_submitted' AND DATE_SUB(NOW(), INTERVAL %d DAY) > c.comment_date_gmt LIMIT 10000"), interval_))
            if not (comment_ids_):
                break
            # end if
            if php_empty(lambda : comment_ids_):
                return
            # end if
            wpdb_.queries = Array()
            for comment_id_ in comment_ids_:
                delete_comment_meta(comment_id_, "akismet_as_submitted")
                do_action("akismet_batch_delete_count", inspect.currentframe().f_code.co_name)
            # end for
            do_action("akismet_delete_commentmeta_batch", php_count(comment_ids_))
        # end while
        if apply_filters("akismet_optimize_table", mt_rand(1, 5000) == 11, wpdb_.commentmeta):
            #// lucky number
            wpdb_.query(str("OPTIMIZE TABLE ") + str(wpdb_.commentmeta))
        # end if
    # end def delete_old_comments_meta
    #// Clear out comments meta that no longer have corresponding comments in the database
    @classmethod
    def delete_orphaned_commentmeta(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        last_meta_id_ = 0
        start_time_ = PHP_SERVER["REQUEST_TIME_FLOAT"] if (php_isset(lambda : PHP_SERVER["REQUEST_TIME_FLOAT"])) else php_microtime(True)
        max_exec_time_ = php_max(php_ini_get("max_execution_time") - 5, 3)
        while True:
            commentmeta_results_ = wpdb_.get_results(wpdb_.prepare(str("SELECT m.meta_id, m.comment_id, m.meta_key FROM ") + str(wpdb_.commentmeta) + str(" as m LEFT JOIN ") + str(wpdb_.comments) + str(" as c USING(comment_id) WHERE c.comment_id IS NULL AND m.meta_id > %d ORDER BY m.meta_id LIMIT 1000"), last_meta_id_))
            if not (commentmeta_results_):
                break
            # end if
            if php_empty(lambda : commentmeta_results_):
                return
            # end if
            wpdb_.queries = Array()
            commentmeta_deleted_ = 0
            for commentmeta_ in commentmeta_results_:
                if "akismet_" == php_substr(commentmeta_.meta_key, 0, 8):
                    delete_comment_meta(commentmeta_.comment_id, commentmeta_.meta_key)
                    do_action("akismet_batch_delete_count", inspect.currentframe().f_code.co_name)
                    commentmeta_deleted_ += 1
                # end if
                last_meta_id_ = commentmeta_.meta_id
            # end for
            do_action("akismet_delete_commentmeta_batch", commentmeta_deleted_)
            #// If we're getting close to max_execution_time, quit for this round.
            if php_microtime(True) - start_time_ > max_exec_time_:
                return
            # end if
        # end while
        if apply_filters("akismet_optimize_table", mt_rand(1, 5000) == 11, wpdb_.commentmeta):
            #// lucky number
            wpdb_.query(str("OPTIMIZE TABLE ") + str(wpdb_.commentmeta))
        # end if
    # end def delete_orphaned_commentmeta
    #// how many approved comments does this author have?
    @classmethod
    def get_user_comments_approved(self, user_id_=None, comment_author_email_=None, comment_author_=None, comment_author_url_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not php_empty(lambda : user_id_)):
            return php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.comments) + str(" WHERE user_id = %d AND comment_approved = 1"), user_id_)))
        # end if
        if (not php_empty(lambda : comment_author_email_)):
            return php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.comments) + str(" WHERE comment_author_email = %s AND comment_author = %s AND comment_author_url = %s AND comment_approved = 1"), comment_author_email_, comment_author_, comment_author_url_)))
        # end if
        return 0
    # end def get_user_comments_approved
    #// get the full comment history for a given comment, as an array in reverse chronological order
    @classmethod
    def get_comment_history(self, comment_id_=None):
        
        
        history_ = get_comment_meta(comment_id_, "akismet_history", False)
        if php_empty(lambda : history_) or php_empty(lambda : history_[0]):
            return False
        # end if
        #// 
        #// To see all variants when testing.
        #// $history[] = array( 'time' => 445856401, 'message' => 'Old versions of Akismet stored the message as a literal string in the commentmeta.', 'event' => null );
        #// $history[] = array( 'time' => 445856402, 'event' => 'recheck-spam' );
        #// $history[] = array( 'time' => 445856403, 'event' => 'check-spam' );
        #// $history[] = array( 'time' => 445856404, 'event' => 'recheck-ham' );
        #// $history[] = array( 'time' => 445856405, 'event' => 'check-ham' );
        #// $history[] = array( 'time' => 445856406, 'event' => 'wp-blacklisted' );
        #// $history[] = array( 'time' => 445856407, 'event' => 'report-spam' );
        #// $history[] = array( 'time' => 445856408, 'event' => 'report-spam', 'user' => 'sam' );
        #// $history[] = array( 'message' => 'sam reported this comment as spam (hardcoded message).', 'time' => 445856400, 'event' => 'report-spam', 'user' => 'sam' );
        #// $history[] = array( 'time' => 445856409, 'event' => 'report-ham', 'user' => 'sam' );
        #// $history[] = array( 'message' => 'sam reported this comment as ham (hardcoded message).', 'time' => 445856400, 'event' => 'report-ham', 'user' => 'sam' );
        #// $history[] = array( 'time' => 445856410, 'event' => 'cron-retry-spam' );
        #// $history[] = array( 'time' => 445856411, 'event' => 'cron-retry-ham' );
        #// $history[] = array( 'time' => 445856412, 'event' => 'check-error' );
        #// $history[] = array( 'time' => 445856413, 'event' => 'check-error', 'meta' => array( 'response' => 'The server was taking a nap.' ) );
        #// $history[] = array( 'time' => 445856414, 'event' => 'recheck-error' ); // Should not generate a message.
        #// $history[] = array( 'time' => 445856415, 'event' => 'recheck-error', 'meta' => array( 'response' => 'The server was taking a nap.' ) );
        #// $history[] = array( 'time' => 445856416, 'event' => 'status-changedtrash' );
        #// $history[] = array( 'time' => 445856417, 'event' => 'status-changedspam' );
        #// $history[] = array( 'time' => 445856418, 'event' => 'status-changedhold' );
        #// $history[] = array( 'time' => 445856419, 'event' => 'status-changedapprove' );
        #// $history[] = array( 'time' => 445856420, 'event' => 'status-changed-trash' );
        #// $history[] = array( 'time' => 445856421, 'event' => 'status-changed-spam' );
        #// $history[] = array( 'time' => 445856422, 'event' => 'status-changed-hold' );
        #// $history[] = array( 'time' => 445856423, 'event' => 'status-changed-approve' );
        #// $history[] = array( 'time' => 445856424, 'event' => 'status-trash', 'user' => 'sam' );
        #// $history[] = array( 'time' => 445856425, 'event' => 'status-spam', 'user' => 'sam' );
        #// $history[] = array( 'time' => 445856426, 'event' => 'status-hold', 'user' => 'sam' );
        #// $history[] = array( 'time' => 445856427, 'event' => 'status-approve', 'user' => 'sam' );
        #//
        usort(history_, Array("Akismet", "_cmp_time"))
        return history_
    # end def get_comment_history
    #// 
    #// Log an event for a given comment, storing it in comment_meta.
    #// 
    #// @param int $comment_id The ID of the relevant comment.
    #// @param string $message The string description of the event. No longer used.
    #// @param string $event The event code.
    #// @param array $meta Metadata about the history entry. e.g., the user that reported or changed the status of a given comment.
    #//
    @classmethod
    def update_comment_history(self, comment_id_=None, message_=None, event_=None, meta_=None):
        if event_ is None:
            event_ = None
        # end if
        if meta_ is None:
            meta_ = None
        # end if
        
        global current_user_
        php_check_if_defined("current_user_")
        user_ = ""
        event_ = Array({"time": self._get_microtime(), "event": event_})
        if php_is_object(current_user_) and (php_isset(lambda : current_user_.user_login)):
            event_["user"] = current_user_.user_login
        # end if
        if (not php_empty(lambda : meta_)):
            event_["meta"] = meta_
        # end if
        #// $unique = false so as to allow multiple values per comment
        r_ = add_comment_meta(comment_id_, "akismet_history", event_, False)
    # end def update_comment_history
    @classmethod
    def check_db_comment(self, id_=None, recheck_reason_="recheck_queue"):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not self.get_api_key()):
            return php_new_class("WP_Error", lambda : WP_Error("akismet-not-configured", __("Akismet is not configured. Please enter an API key.", "akismet")))
        # end if
        c_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_ID = %d"), id_), ARRAY_A)
        if (not c_):
            return php_new_class("WP_Error", lambda : WP_Error("invalid-comment-id", __("Comment not found.", "akismet")))
        # end if
        c_["user_ip"] = c_["comment_author_IP"]
        c_["user_agent"] = c_["comment_agent"]
        c_["referrer"] = ""
        c_["blog"] = get_option("home")
        c_["blog_lang"] = get_locale()
        c_["blog_charset"] = get_option("blog_charset")
        c_["permalink"] = get_permalink(c_["comment_post_ID"])
        c_["recheck_reason"] = recheck_reason_
        c_["user_role"] = ""
        if (not php_empty(lambda : c_["user_ID"])):
            c_["user_role"] = Akismet.get_user_roles(c_["user_ID"])
        # end if
        if self.is_test_mode():
            c_["is_test"] = "true"
        # end if
        response_ = self.http_post(Akismet.build_query(c_), "comment-check")
        if (not php_empty(lambda : response_[1])):
            return response_[1]
        # end if
        return False
    # end def check_db_comment
    @classmethod
    def recheck_comment(self, id_=None, recheck_reason_="recheck_queue"):
        
        
        add_comment_meta(id_, "akismet_rechecking", True)
        api_response_ = self.check_db_comment(id_, recheck_reason_)
        delete_comment_meta(id_, "akismet_rechecking")
        if is_wp_error(api_response_):
            pass
        else:
            if "true" == api_response_:
                wp_set_comment_status(id_, "spam")
                update_comment_meta(id_, "akismet_result", "true")
                delete_comment_meta(id_, "akismet_error")
                delete_comment_meta(id_, "akismet_delayed_moderation_email")
                Akismet.update_comment_history(id_, "", "recheck-spam")
            elif "false" == api_response_:
                update_comment_meta(id_, "akismet_result", "false")
                delete_comment_meta(id_, "akismet_error")
                delete_comment_meta(id_, "akismet_delayed_moderation_email")
                Akismet.update_comment_history(id_, "", "recheck-ham")
            else:
                #// abnormal result: error
                update_comment_meta(id_, "akismet_result", "error")
                Akismet.update_comment_history(id_, "", "recheck-error", Array({"response": php_substr(api_response_, 0, 50)}))
            # end if
        # end if
        return api_response_
    # end def recheck_comment
    @classmethod
    def transition_comment_status(self, new_status_=None, old_status_=None, comment_=None):
        
        
        if new_status_ == old_status_:
            return
        # end if
        if "spam" == new_status_ or "spam" == old_status_:
            #// Clear the cache of the "X comments in your spam queue" count on the dashboard.
            wp_cache_delete("akismet_spam_count", "widget")
        # end if
        #// # we don't need to record a history item for deleted comments
        if new_status_ == "delete":
            return
        # end if
        if (not current_user_can("edit_post", comment_.comment_post_ID)) and (not current_user_can("moderate_comments")):
            return
        # end if
        if php_defined("WP_IMPORTING") and WP_IMPORTING == True:
            return
        # end if
        #// if this is present, it means the status has been changed by a re-check, not an explicit user action
        if get_comment_meta(comment_.comment_ID, "akismet_rechecking"):
            return
        # end if
        #// Assumption alert:
        #// We want to submit comments to Akismet only when a moderator explicitly spams or approves it - not if the status
        #// is changed automatically by another plugin.  Unfortunately WordPress doesn't provide an unambiguous way to
        #// determine why the transition_comment_status action was triggered.  And there are several different ways by which
        #// to spam and unspam comments: bulk actions, ajax, links in moderation emails, the dashboard, and perhaps others.
        #// We'll assume that this is an explicit user action if certain POST/GET variables exist.
        if (php_isset(lambda : PHP_POST["status"])) and php_in_array(PHP_POST["status"], Array("spam", "unspam", "approved")) or (php_isset(lambda : PHP_POST["spam"])) and php_int(PHP_POST["spam"]) == 1 or (php_isset(lambda : PHP_POST["unspam"])) and php_int(PHP_POST["unspam"]) == 1 or (php_isset(lambda : PHP_POST["comment_status"])) and php_in_array(PHP_POST["comment_status"], Array("spam", "unspam")) or (php_isset(lambda : PHP_REQUEST["action"])) and php_in_array(PHP_REQUEST["action"], Array("spam", "unspam", "spamcomment", "unspamcomment")) or (php_isset(lambda : PHP_POST["action"])) and php_in_array(PHP_POST["action"], Array("editedcomment")) or (php_isset(lambda : PHP_REQUEST["for"])) and "jetpack" == PHP_REQUEST["for"] and (not php_defined("IS_WPCOM")) or (not IS_WPCOM) or php_defined("REST_API_REQUEST") and REST_API_REQUEST or php_defined("REST_REQUEST") and REST_REQUEST:
            if new_status_ == "spam" and old_status_ == "approved" or old_status_ == "unapproved" or (not old_status_):
                return self.submit_spam_comment(comment_.comment_ID)
            elif old_status_ == "spam" and new_status_ == "approved" or new_status_ == "unapproved":
                return self.submit_nonspam_comment(comment_.comment_ID)
            # end if
        # end if
        self.update_comment_history(comment_.comment_ID, "", "status-" + new_status_)
    # end def transition_comment_status
    @classmethod
    def submit_spam_comment(self, comment_id_=None):
        
        
        global wpdb_
        global current_user_
        global current_site_
        php_check_if_defined("wpdb_","current_user_","current_site_")
        comment_id_ = php_int(comment_id_)
        comment_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_ID = %d"), comment_id_))
        if (not comment_):
            #// it was deleted
            return
        # end if
        if "spam" != comment_.comment_approved:
            return
        # end if
        self.update_comment_history(comment_id_, "", "report-spam")
        #// If the user hasn't configured Akismet, there's nothing else to do at this point.
        if (not self.get_api_key()):
            return
        # end if
        #// use the original version stored in comment_meta if available
        as_submitted_ = self.sanitize_comment_as_submitted(get_comment_meta(comment_id_, "akismet_as_submitted", True))
        if as_submitted_ and php_is_array(as_submitted_) and (php_isset(lambda : as_submitted_["comment_content"])):
            comment_ = php_array_merge(comment_, as_submitted_)
        # end if
        comment_.blog = get_option("home")
        comment_.blog_lang = get_locale()
        comment_.blog_charset = get_option("blog_charset")
        comment_.permalink = get_permalink(comment_.comment_post_ID)
        if php_is_object(current_user_):
            comment_.reporter = current_user_.user_login
        # end if
        if php_is_object(current_site_):
            comment_.site_domain = current_site_.domain
        # end if
        comment_.user_role = ""
        if (not php_empty(lambda : comment_.user_ID)):
            comment_.user_role = Akismet.get_user_roles(comment_.user_ID)
        # end if
        if self.is_test_mode():
            comment_.is_test = "true"
        # end if
        post_ = get_post(comment_.comment_post_ID)
        if (not php_is_null(post_)):
            comment_.comment_post_modified_gmt = post_.post_modified_gmt
        # end if
        response_ = Akismet.http_post(Akismet.build_query(comment_), "submit-spam")
        update_comment_meta(comment_id_, "akismet_user_result", "true")
        if comment_.reporter:
            update_comment_meta(comment_id_, "akismet_user", comment_.reporter)
        # end if
        do_action("akismet_submit_spam_comment", comment_id_, response_[1])
    # end def submit_spam_comment
    @classmethod
    def submit_nonspam_comment(self, comment_id_=None):
        
        
        global wpdb_
        global current_user_
        global current_site_
        php_check_if_defined("wpdb_","current_user_","current_site_")
        comment_id_ = php_int(comment_id_)
        comment_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_ID = %d"), comment_id_))
        if (not comment_):
            #// it was deleted
            return
        # end if
        self.update_comment_history(comment_id_, "", "report-ham")
        #// If the user hasn't configured Akismet, there's nothing else to do at this point.
        if (not self.get_api_key()):
            return
        # end if
        #// use the original version stored in comment_meta if available
        as_submitted_ = self.sanitize_comment_as_submitted(get_comment_meta(comment_id_, "akismet_as_submitted", True))
        if as_submitted_ and php_is_array(as_submitted_) and (php_isset(lambda : as_submitted_["comment_content"])):
            comment_ = php_array_merge(comment_, as_submitted_)
        # end if
        comment_.blog = get_option("home")
        comment_.blog_lang = get_locale()
        comment_.blog_charset = get_option("blog_charset")
        comment_.permalink = get_permalink(comment_.comment_post_ID)
        comment_.user_role = ""
        if php_is_object(current_user_):
            comment_.reporter = current_user_.user_login
        # end if
        if php_is_object(current_site_):
            comment_.site_domain = current_site_.domain
        # end if
        if (not php_empty(lambda : comment_.user_ID)):
            comment_.user_role = Akismet.get_user_roles(comment_.user_ID)
        # end if
        if Akismet.is_test_mode():
            comment_.is_test = "true"
        # end if
        post_ = get_post(comment_.comment_post_ID)
        if (not php_is_null(post_)):
            comment_.comment_post_modified_gmt = post_.post_modified_gmt
        # end if
        response_ = self.http_post(Akismet.build_query(comment_), "submit-ham")
        update_comment_meta(comment_id_, "akismet_user_result", "false")
        if comment_.reporter:
            update_comment_meta(comment_id_, "akismet_user", comment_.reporter)
        # end if
        do_action("akismet_submit_nonspam_comment", comment_id_, response_[1])
    # end def submit_nonspam_comment
    @classmethod
    def cron_recheck(self):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        api_key_ = self.get_api_key()
        status_ = self.verify_key(api_key_)
        if get_option("akismet_alert_code") or status_ == "invalid":
            #// since there is currently a problem with the key, reschedule a check for 6 hours hence
            wp_schedule_single_event(time() + 21600, "akismet_schedule_cron_recheck")
            do_action("akismet_scheduled_recheck", "key-problem-" + get_option("akismet_alert_code") + "-" + status_)
            return False
        # end if
        delete_option("akismet_available_servers")
        comment_errors_ = wpdb_.get_col(str("SELECT comment_id FROM ") + str(wpdb_.commentmeta) + str(" WHERE meta_key = 'akismet_error'    LIMIT 100"))
        load_plugin_textdomain("akismet")
        for comment_id_ in comment_errors_:
            #// if the comment no longer exists, or is too old, remove the meta entry from the queue to avoid getting stuck
            comment_ = get_comment(comment_id_)
            if (not comment_) or strtotime(comment_.comment_date_gmt) < strtotime("-15 days") or comment_.comment_approved != "0":
                delete_comment_meta(comment_id_, "akismet_error")
                delete_comment_meta(comment_id_, "akismet_delayed_moderation_email")
                continue
            # end if
            add_comment_meta(comment_id_, "akismet_rechecking", True)
            status_ = self.check_db_comment(comment_id_, "retry")
            event_ = ""
            if status_ == "true":
                event_ = "cron-retry-spam"
            elif status_ == "false":
                event_ = "cron-retry-ham"
            # end if
            #// If we got back a legit response then update the comment history
            #// other wise just bail now and try again later.  No point in
            #// re-trying all the comments once we hit one failure.
            if (not php_empty(lambda : event_)):
                delete_comment_meta(comment_id_, "akismet_error")
                self.update_comment_history(comment_id_, "", event_)
                update_comment_meta(comment_id_, "akismet_result", status_)
                #// make sure the comment status is still pending.  if it isn't, that means the user has already moved it elsewhere.
                comment_ = get_comment(comment_id_)
                if comment_ and "unapproved" == wp_get_comment_status(comment_id_):
                    if status_ == "true":
                        wp_spam_comment(comment_id_)
                    elif status_ == "false":
                        #// comment is good, but it's still in the pending queue.  depending on the moderation settings
                        #// we may need to change it to approved.
                        if check_comment(comment_.comment_author, comment_.comment_author_email, comment_.comment_author_url, comment_.comment_content, comment_.comment_author_IP, comment_.comment_agent, comment_.comment_type):
                            wp_set_comment_status(comment_id_, 1)
                        else:
                            if get_comment_meta(comment_id_, "akismet_delayed_moderation_email", True):
                                wp_notify_moderator(comment_id_)
                            # end if
                        # end if
                    # end if
                # end if
                delete_comment_meta(comment_id_, "akismet_delayed_moderation_email")
            else:
                #// If this comment has been pending moderation for longer than MAX_DELAY_BEFORE_MODERATION_EMAIL,
                #// send a moderation email now.
                if php_intval(gmdate("U")) - strtotime(comment_.comment_date_gmt) < self.MAX_DELAY_BEFORE_MODERATION_EMAIL:
                    delete_comment_meta(comment_id_, "akismet_delayed_moderation_email")
                    wp_notify_moderator(comment_id_)
                # end if
                delete_comment_meta(comment_id_, "akismet_rechecking")
                wp_schedule_single_event(time() + 1200, "akismet_schedule_cron_recheck")
                do_action("akismet_scheduled_recheck", "check-db-comment-" + status_)
                return
            # end if
            delete_comment_meta(comment_id_, "akismet_rechecking")
        # end for
        remaining_ = wpdb_.get_var(str("SELECT COUNT(*) FROM ") + str(wpdb_.commentmeta) + str(" WHERE meta_key = 'akismet_error'"))
        if remaining_ and (not wp_next_scheduled("akismet_schedule_cron_recheck")):
            wp_schedule_single_event(time() + 1200, "akismet_schedule_cron_recheck")
            do_action("akismet_scheduled_recheck", "remaining")
        # end if
    # end def cron_recheck
    @classmethod
    def fix_scheduled_recheck(self):
        
        
        future_check_ = wp_next_scheduled("akismet_schedule_cron_recheck")
        if (not future_check_):
            return
        # end if
        if get_option("akismet_alert_code") > 0:
            return
        # end if
        check_range_ = time() + 1200
        if future_check_ > check_range_:
            wp_clear_scheduled_hook("akismet_schedule_cron_recheck")
            wp_schedule_single_event(time() + 300, "akismet_schedule_cron_recheck")
            do_action("akismet_scheduled_recheck", "fix-scheduled-recheck")
        # end if
    # end def fix_scheduled_recheck
    @classmethod
    def add_comment_nonce(self, post_id_=None):
        
        
        #// 
        #// To disable the Akismet comment nonce, add a filter for the 'akismet_comment_nonce' tag
        #// and return any string value that is not 'true' or '' (empty string).
        #// 
        #// Don't return boolean false, because that implies that the 'akismet_comment_nonce' option
        #// has not been set and that Akismet should just choose the default behavior for that
        #// situation.
        #//
        if (not self.get_api_key()):
            return
        # end if
        akismet_comment_nonce_option_ = apply_filters("akismet_comment_nonce", get_option("akismet_comment_nonce"))
        if akismet_comment_nonce_option_ == "true" or akismet_comment_nonce_option_ == "":
            php_print("<p style=\"display: none;\">")
            wp_nonce_field("akismet_comment_nonce_" + post_id_, "akismet_comment_nonce", False)
            php_print("</p>")
        # end if
    # end def add_comment_nonce
    @classmethod
    def is_test_mode(self):
        
        
        return php_defined("AKISMET_TEST_MODE") and AKISMET_TEST_MODE
    # end def is_test_mode
    @classmethod
    def allow_discard(self):
        
        
        if php_defined("DOING_AJAX") and DOING_AJAX:
            return False
        # end if
        if is_user_logged_in():
            return False
        # end if
        return get_option("akismet_strictness") == "1"
    # end def allow_discard
    @classmethod
    def get_ip_address(self):
        
        
        return PHP_SERVER["REMOTE_ADDR"] if (php_isset(lambda : PHP_SERVER["REMOTE_ADDR"])) else None
    # end def get_ip_address
    #// 
    #// Do these two comments, without checking the comment_ID, "match"?
    #// 
    #// @param mixed $comment1 A comment object or array.
    #// @param mixed $comment2 A comment object or array.
    #// @return bool Whether the two comments should be treated as the same comment.
    #//
    def comments_match(self, comment1_=None, comment2_=None):
        
        
        comment1_ = comment1_
        comment2_ = comment2_
        #// Set default values for these strings that we check in order to simplify
        #// the checks and avoid PHP warnings.
        if (not (php_isset(lambda : comment1_["comment_author"]))):
            comment1_["comment_author"] = ""
        # end if
        if (not (php_isset(lambda : comment2_["comment_author"]))):
            comment2_["comment_author"] = ""
        # end if
        if (not (php_isset(lambda : comment1_["comment_author_email"]))):
            comment1_["comment_author_email"] = ""
        # end if
        if (not (php_isset(lambda : comment2_["comment_author_email"]))):
            comment2_["comment_author_email"] = ""
        # end if
        comments_match_ = (php_isset(lambda : comment1_["comment_post_ID"]) and php_isset(lambda : comment2_["comment_post_ID"])) and php_intval(comment1_["comment_post_ID"]) == php_intval(comment2_["comment_post_ID"]) and php_substr(comment1_["comment_author"], 0, 248) == php_substr(comment2_["comment_author"], 0, 248) or php_substr(stripslashes(comment1_["comment_author"]), 0, 248) == php_substr(comment2_["comment_author"], 0, 248) or php_substr(comment1_["comment_author"], 0, 248) == php_substr(stripslashes(comment2_["comment_author"]), 0, 248) or (not comment1_["comment_author"]) and php_strlen(comment2_["comment_author"]) > 248 or (not comment2_["comment_author"]) and php_strlen(comment1_["comment_author"]) > 248 and php_substr(comment1_["comment_author_email"], 0, 93) == php_substr(comment2_["comment_author_email"], 0, 93) or php_substr(stripslashes(comment1_["comment_author_email"]), 0, 93) == php_substr(comment2_["comment_author_email"], 0, 93) or php_substr(comment1_["comment_author_email"], 0, 93) == php_substr(stripslashes(comment2_["comment_author_email"]), 0, 93) or (not comment1_["comment_author_email"]) and php_strlen(comment2_["comment_author_email"]) > 100 or (not comment2_["comment_author_email"]) and php_strlen(comment1_["comment_author_email"]) > 100
        return comments_match_
    # end def comments_match
    #// Does the supplied comment match the details of the one most recently stored in self::$last_comment?
    @classmethod
    def matches_last_comment(self, comment_=None):
        
        
        return self.comments_match(self.last_comment, comment_)
    # end def matches_last_comment
    def get_user_agent(self):
        
        
        return PHP_SERVER["HTTP_USER_AGENT"] if (php_isset(lambda : PHP_SERVER["HTTP_USER_AGENT"])) else None
    # end def get_user_agent
    def get_referer(self):
        
        
        return PHP_SERVER["HTTP_REFERER"] if (php_isset(lambda : PHP_SERVER["HTTP_REFERER"])) else None
    # end def get_referer
    #// return a comma-separated list of role names for the given user
    @classmethod
    def get_user_roles(self, user_id_=None):
        
        
        roles_ = False
        if (not php_class_exists("WP_User")):
            return False
        # end if
        if user_id_ > 0:
            comment_user_ = php_new_class("WP_User", lambda : WP_User(user_id_))
            if (php_isset(lambda : comment_user_.roles)):
                roles_ = php_join(",", comment_user_.roles)
            # end if
        # end if
        if is_multisite() and is_super_admin(user_id_):
            if php_empty(lambda : roles_):
                roles_ = "super_admin"
            else:
                comment_user_.roles[-1] = "super_admin"
                roles_ = php_join(",", comment_user_.roles)
            # end if
        # end if
        return roles_
    # end def get_user_roles
    #// filter handler used to return a spam result to pre_comment_approved
    @classmethod
    def last_comment_status(self, approved_=None, comment_=None):
        
        
        if php_is_null(self.last_comment_result):
            #// We didn't have reason to store the result of the last check.
            return approved_
        # end if
        #// Only do this if it's the correct comment
        if (not self.matches_last_comment(comment_)):
            self.log(str("comment_is_spam mismatched comment, returning unaltered ") + str(approved_))
            return approved_
        # end if
        if "trash" == approved_:
            #// If the last comment we checked has had its approval set to 'trash',
            #// then it failed the comment blacklist check. Let that blacklist override
            #// the spam check, since users have the (valid) expectation that when
            #// they fill out their blacklists, comments that match it will always
            #// end up in the trash.
            return approved_
        # end if
        #// bump the counter here instead of when the filter is added to reduce the possibility of overcounting
        incr_ = apply_filters("akismet_spam_count_incr", 1)
        if incr_:
            update_option("akismet_spam_count", get_option("akismet_spam_count") + incr_)
        # end if
        return self.last_comment_result
    # end def last_comment_status
    #// 
    #// If Akismet is temporarily unreachable, we don't want to "spam" the blogger with
    #// moderation emails for comments that will be automatically cleared or spammed on
    #// the next retry.
    #// 
    #// For comments that will be rechecked later, empty the list of email addresses that
    #// the moderation email would be sent to.
    #// 
    #// @param array $emails An array of email addresses that the moderation email will be sent to.
    #// @param int $comment_id The ID of the relevant comment.
    #// @return array An array of email addresses that the moderation email will be sent to.
    #//
    @classmethod
    def disable_moderation_emails_if_unreachable(self, emails_=None, comment_id_=None):
        
        
        if (not php_empty(lambda : self.prevent_moderation_email_for_these_comments)) and (not php_empty(lambda : emails_)):
            comment_ = get_comment(comment_id_)
            for possible_match_ in self.prevent_moderation_email_for_these_comments:
                if self.comments_match(possible_match_, comment_):
                    update_comment_meta(comment_id_, "akismet_delayed_moderation_email", True)
                    return Array()
                # end if
            # end for
        # end if
        return emails_
    # end def disable_moderation_emails_if_unreachable
    @classmethod
    def _cmp_time(self, a_=None, b_=None):
        
        
        return -1 if a_["time"] > b_["time"] else 1
    # end def _cmp_time
    @classmethod
    def _get_microtime(self):
        
        
        mtime_ = php_explode(" ", php_microtime())
        return mtime_[1] + mtime_[0]
    # end def _get_microtime
    #// 
    #// Make a POST request to the Akismet API.
    #// 
    #// @param string $request The body of the request.
    #// @param string $path The path for the request.
    #// @param string $ip The specific IP address to hit.
    #// @return array A two-member array consisting of the headers and the response body, both empty in the case of a failure.
    #//
    @classmethod
    def http_post(self, request_=None, path_=None, ip_=None):
        if ip_ is None:
            ip_ = None
        # end if
        
        akismet_ua_ = php_sprintf("WordPress/%s | Akismet/%s", PHP_GLOBALS["wp_version"], constant("AKISMET_VERSION"))
        akismet_ua_ = apply_filters("akismet_ua", akismet_ua_)
        content_length_ = php_strlen(request_)
        api_key_ = self.get_api_key()
        host_ = self.API_HOST
        if (not php_empty(lambda : api_key_)):
            host_ = api_key_ + "." + host_
        # end if
        http_host_ = host_
        #// use a specific IP if provided
        #// needed by Akismet_Admin::check_server_connectivity()
        if ip_ and long2ip(ip2long(ip_)):
            http_host_ = ip_
        # end if
        http_args_ = Array({"body": request_, "headers": Array({"Content-Type": "application/x-www-form-urlencoded; charset=" + get_option("blog_charset"), "Host": host_, "User-Agent": akismet_ua_})}, {"httpversion": "1.0", "timeout": 15})
        akismet_url_ = http_akismet_url_ = str("http://") + str(http_host_) + str("/1.1/") + str(path_)
        #// 
        #// Try SSL first; if that fails, try without it and don't try it again for a while.
        #//
        ssl_ = ssl_failed_ = False
        #// Check if SSL requests were disabled fewer than X hours ago.
        ssl_disabled_ = get_option("akismet_ssl_disabled")
        if ssl_disabled_ and ssl_disabled_ < time() - 60 * 60 * 24:
            #// 24 hours
            ssl_disabled_ = False
            delete_option("akismet_ssl_disabled")
        else:
            if ssl_disabled_:
                do_action("akismet_ssl_disabled")
            # end if
        # end if
        ssl_ = wp_http_supports(Array("ssl"))
        if (not ssl_disabled_) and ssl_:
            akismet_url_ = set_url_scheme(akismet_url_, "https")
            do_action("akismet_https_request_pre")
        # end if
        response_ = wp_remote_post(akismet_url_, http_args_)
        Akismet.log(php_compact("akismet_url_", "http_args_", "response_"))
        if ssl_ and is_wp_error(response_):
            do_action("akismet_https_request_failure", response_)
            #// Intermittent connection problems may cause the first HTTPS
            #// request to fail and subsequent HTTP requests to succeed randomly.
            #// Retry the HTTPS request once before disabling SSL for a time.
            response_ = wp_remote_post(akismet_url_, http_args_)
            Akismet.log(php_compact("akismet_url_", "http_args_", "response_"))
            if is_wp_error(response_):
                ssl_failed_ = True
                do_action("akismet_https_request_failure", response_)
                do_action("akismet_http_request_pre")
                #// Try the request again without SSL.
                response_ = wp_remote_post(http_akismet_url_, http_args_)
                Akismet.log(php_compact("http_akismet_url_", "http_args_", "response_"))
            # end if
        # end if
        if is_wp_error(response_):
            do_action("akismet_request_failure", response_)
            return Array("", "")
        # end if
        if ssl_failed_:
            #// The request failed when using SSL but succeeded without it. Disable SSL for future requests.
            update_option("akismet_ssl_disabled", time())
            do_action("akismet_https_disabled")
        # end if
        simplified_response_ = Array(response_["headers"], response_["body"])
        self.update_alert(simplified_response_)
        return simplified_response_
    # end def http_post
    #// given a response from an API call like check_key_status(), update the alert code options if an alert is present.
    @classmethod
    def update_alert(self, response_=None):
        
        
        code_ = msg_ = None
        if (php_isset(lambda : response_[0]["x-akismet-alert-code"])):
            code_ = response_[0]["x-akismet-alert-code"]
            msg_ = response_[0]["x-akismet-alert-msg"]
        # end if
        #// only call update_option() if the value has changed
        if code_ != get_option("akismet_alert_code"):
            if (not code_):
                delete_option("akismet_alert_code")
                delete_option("akismet_alert_msg")
            else:
                update_option("akismet_alert_code", code_)
                update_option("akismet_alert_msg", msg_)
            # end if
        # end if
    # end def update_alert
    @classmethod
    def load_form_js(self):
        
        
        if php_function_exists("is_amp_endpoint") and is_amp_endpoint():
            return
        # end if
        if (not self.get_api_key()):
            return
        # end if
        wp_register_script("akismet-form", plugin_dir_url(__FILE__) + "_inc/form.js", Array(), AKISMET_VERSION, True)
        wp_enqueue_script("akismet-form")
    # end def load_form_js
    #// 
    #// Mark form.js as async. Because nothing depends on it, it can run at any time
    #// after it's loaded, and the browser won't have to wait for it to load to continue
    #// parsing the rest of the page.
    #//
    @classmethod
    def set_form_js_async(self, tag_=None, handle_=None, src_=None):
        
        
        if "akismet-form" != handle_:
            return tag_
        # end if
        return php_preg_replace("/^<script /i", "<script async=\"async\" ", tag_)
    # end def set_form_js_async
    @classmethod
    def inject_ak_js(self, fields_=None):
        
        
        php_print("<p style=\"display: none;\">")
        php_print("<input type=\"hidden\" id=\"ak_js\" name=\"ak_js\" value=\"" + mt_rand(0, 250) + "\"/>")
        php_print("</p>")
    # end def inject_ak_js
    def bail_on_activation(self, message_=None, deactivate_=None):
        if deactivate_ is None:
            deactivate_ = True
        # end if
        
        php_print("""<!doctype html>
        <html>
        <head>
        <meta charset=\"""")
        bloginfo("charset")
        php_print("""\" />
        <style>
        * {
        text-align: center;
        margin: 0;
        padding: 0;
        font-family: \"Lucida Grande\",Verdana,Arial,\"Bitstream Vera Sans\",sans-serif;
        }
        p {
        margin-top: 1em;
        font-size: 18px;
        }
        </style>
        </head>
        <body>
        <p>""")
        php_print(esc_html(message_))
        php_print("""</p>
        </body>
        </html>
        """)
        if deactivate_:
            plugins_ = get_option("active_plugins")
            akismet_ = plugin_basename(AKISMET__PLUGIN_DIR + "akismet.php")
            update_ = False
            for i_,plugin_ in plugins_.items():
                if plugin_ == akismet_:
                    plugins_[i_] = False
                    update_ = True
                # end if
            # end for
            if update_:
                update_option("active_plugins", php_array_filter(plugins_))
            # end if
        # end if
        php_exit(0)
    # end def bail_on_activation
    @classmethod
    def view(self, name_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        args_ = apply_filters("akismet_view_arguments", args_, name_)
        for key_,val_ in args_.items():
            key__ = val_
        # end for
        load_plugin_textdomain("akismet")
        file_ = AKISMET__PLUGIN_DIR + "views/" + name_ + ".php"
        php_include_file(file_, once=False)
    # end def view
    #// 
    #// Attached to activate_{ plugin_basename( __FILES__ ) } by register_activation_hook()
    #// @static
    #//
    @classmethod
    def plugin_activation(self):
        
        
        if php_version_compare(PHP_GLOBALS["wp_version"], AKISMET__MINIMUM_WP_VERSION, "<"):
            load_plugin_textdomain("akismet")
            message_ = "<strong>" + php_sprintf(esc_html__("Akismet %s requires WordPress %s or higher.", "akismet"), AKISMET_VERSION, AKISMET__MINIMUM_WP_VERSION) + "</strong> " + php_sprintf(__("Please <a href=\"%1$s\">upgrade WordPress</a> to a current version, or <a href=\"%2$s\">downgrade to version 2.4 of the Akismet plugin</a>.", "akismet"), "https://codex.wordpress.org/Upgrading_WordPress", "https://wordpress.org/extend/plugins/akismet/download/")
            Akismet.bail_on_activation(message_)
        elif (not php_empty(lambda : PHP_SERVER["SCRIPT_NAME"])) and False != php_strpos(PHP_SERVER["SCRIPT_NAME"], "/wp-admin/plugins.php"):
            add_option("Activated_Akismet", True)
        # end if
    # end def plugin_activation
    #// 
    #// Removes all connection options
    #// @static
    #//
    @classmethod
    def plugin_deactivation(self):
        
        
        self.deactivate_key(self.get_api_key())
        #// Remove any scheduled cron jobs.
        akismet_cron_events_ = Array("akismet_schedule_cron_recheck", "akismet_scheduled_delete")
        for akismet_cron_event_ in akismet_cron_events_:
            timestamp_ = wp_next_scheduled(akismet_cron_event_)
            if timestamp_:
                wp_unschedule_event(timestamp_, akismet_cron_event_)
            # end if
        # end for
    # end def plugin_deactivation
    #// 
    #// Essentially a copy of WP's build_query but one that doesn't expect pre-urlencoded values.
    #// 
    #// @param array $args An array of key => value pairs
    #// @return string A string ready for use as a URL query string.
    #//
    @classmethod
    def build_query(self, args_=None):
        
        
        return _http_build_query(args_, "", "&")
    # end def build_query
    #// 
    #// Log debugging info to the error log.
    #// 
    #// Enabled when WP_DEBUG_LOG is enabled (and WP_DEBUG, since according to
    #// core, "WP_DEBUG_DISPLAY and WP_DEBUG_LOG perform no function unless
    #// WP_DEBUG is true), but can be disabled via the akismet_debug_log filter.
    #// 
    #// @param mixed $akismet_debug The data to log.
    #//
    @classmethod
    def log(self, akismet_debug_=None):
        
        
        if apply_filters("akismet_debug_log", php_defined("WP_DEBUG") and WP_DEBUG and php_defined("WP_DEBUG_LOG") and WP_DEBUG_LOG and php_defined("AKISMET_DEBUG") and AKISMET_DEBUG):
            php_error_log(print_r(php_compact("akismet_debug_"), True))
        # end if
    # end def log
    @classmethod
    def pre_check_pingback(self, method_=None):
        
        
        if method_ != "pingback.ping":
            return
        # end if
        global wp_xmlrpc_server_
        php_check_if_defined("wp_xmlrpc_server_")
        if (not php_is_object(wp_xmlrpc_server_)):
            return False
        # end if
        #// Lame: tightly coupled with the IXR class.
        args_ = wp_xmlrpc_server_.message.params
        if (not php_empty(lambda : args_[1])):
            post_id_ = url_to_postid(args_[1])
            #// If pingbacks aren't open on this post, we'll still check whether this request is part of a potential DDOS,
            #// but indicate to the server that pingbacks are indeed closed so we don't include this request in the user's stats,
            #// since the user has already done their part by disabling pingbacks.
            pingbacks_closed_ = False
            post_ = get_post(post_id_)
            if (not post_) or (not pings_open(post_)):
                pingbacks_closed_ = True
            # end if
            comment_ = Array({"comment_author_url": args_[0], "comment_post_ID": post_id_, "comment_author": "", "comment_author_email": "", "comment_content": "", "comment_type": "pingback", "akismet_pre_check": "1", "comment_pingback_target": args_[1], "pingbacks_closed": "1" if pingbacks_closed_ else "0"})
            comment_ = Akismet.auto_check_comment(comment_)
            if (php_isset(lambda : comment_["akismet_result"])) and "true" == comment_["akismet_result"]:
                #// Lame: tightly coupled with the IXR classes. Unfortunately the action provides no context and no way to return anything.
                wp_xmlrpc_server_.error(php_new_class("IXR_Error", lambda : IXR_Error(0, "Invalid discovery target")))
            # end if
        # end if
    # end def pre_check_pingback
    #// 
    #// Ensure that we are loading expected scalar values from akismet_as_submitted commentmeta.
    #// 
    #// @param mixed $meta_value
    #// @return mixed
    #//
    def sanitize_comment_as_submitted(self, meta_value_=None):
        
        
        if php_empty(lambda : meta_value_):
            return meta_value_
        # end if
        meta_value_ = meta_value_
        for key_,value_ in meta_value_.items():
            if (not (php_isset(lambda : self.comment_as_submitted_allowed_keys[key_]))) or (not php_is_scalar(value_)):
                meta_value_[key_] = None
            # end if
        # end for
        return meta_value_
    # end def sanitize_comment_as_submitted
    @classmethod
    def predefined_api_key(self):
        
        
        if php_defined("WPCOM_API_KEY"):
            return True
        # end if
        return apply_filters("akismet_predefined_api_key", False)
    # end def predefined_api_key
    #// 
    #// Controls the display of a privacy related notice underneath the comment form using the `akismet_comment_form_privacy_notice` option and filter respectively.
    #// Default is top not display the notice, leaving the choice to site admins, or integrators.
    #//
    @classmethod
    def display_comment_form_privacy_notice(self):
        
        
        if "display" != apply_filters("akismet_comment_form_privacy_notice", get_option("akismet_comment_form_privacy_notice", "hide")):
            return
        # end if
        php_print(apply_filters("akismet_comment_form_privacy_notice_markup", "<p class=\"akismet_comment_form_privacy_notice\">" + php_sprintf(__("This site uses Akismet to reduce spam. <a href=\"%s\" target=\"_blank\" rel=\"nofollow noopener\">Learn how your comment data is processed</a>.", "akismet"), "https://akismet.com/privacy/") + "</p>"))
    # end def display_comment_form_privacy_notice
# end class Akismet
