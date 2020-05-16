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
class Akismet():
    API_HOST = "rest.akismet.com"
    API_PORT = 80
    MAX_DELAY_BEFORE_MODERATION_EMAIL = 86400
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
    def check_key_status(self, key=None, ip=None):
        
        return self.http_post(Akismet.build_query(Array({"key": key, "blog": get_option("home")})), "verify-key", ip)
    # end def check_key_status
    @classmethod
    def verify_key(self, key=None, ip=None):
        
        #// Shortcut for obviously invalid keys.
        if php_strlen(key) != 12:
            return "invalid"
        # end if
        response = self.check_key_status(key, ip)
        if response[1] != "valid" and response[1] != "invalid":
            return "failed"
        # end if
        return response[1]
    # end def verify_key
    @classmethod
    def deactivate_key(self, key=None):
        
        response = self.http_post(Akismet.build_query(Array({"key": key, "blog": get_option("home")})), "deactivate")
        if response[1] != "deactivated":
            return "failed"
        # end if
        return response[1]
    # end def deactivate_key
    #// 
    #// Add the akismet option to the Jetpack options management whitelist.
    #// 
    #// @param array $options The list of whitelisted option names.
    #// @return array The updated whitelist
    #//
    @classmethod
    def add_to_jetpack_options_whitelist(self, options=None):
        
        options[-1] = "wordpress_api_key"
        return options
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
    def updated_option(self, old_value=None, value=None):
        
        #// Not an API call
        if (not php_class_exists("WPCOM_JSON_API_Update_Option_Endpoint")):
            return
        # end if
        #// Only run the registration if the old key is different.
        if old_value != value:
            self.verify_key(value)
        # end if
    # end def updated_option
    #// 
    #// Treat the creation of an API key the same as updating the API key to a new value.
    #// 
    #// @param mixed  $option_name   Will always be "wordpress_api_key", until something else hooks in here.
    #// @param mixed  $value         The option value.
    #//
    @classmethod
    def added_option(self, option_name=None, value=None):
        
        if "wordpress_api_key" == option_name:
            return self.updated_option("", value)
        # end if
    # end def added_option
    @classmethod
    def rest_auto_check_comment(self, commentdata=None):
        
        self.is_rest_api_call = True
        return self.auto_check_comment(commentdata)
    # end def rest_auto_check_comment
    @classmethod
    def auto_check_comment(self, commentdata=None):
        
        #// If no key is configured, then there's no point in doing any of this.
        if (not self.get_api_key()):
            return commentdata
        # end if
        self.last_comment_result = None
        comment = commentdata
        comment["user_ip"] = self.get_ip_address()
        comment["user_agent"] = self.get_user_agent()
        comment["referrer"] = self.get_referer()
        comment["blog"] = get_option("home")
        comment["blog_lang"] = get_locale()
        comment["blog_charset"] = get_option("blog_charset")
        comment["permalink"] = get_permalink(comment["comment_post_ID"])
        if (not php_empty(lambda : comment["user_ID"])):
            comment["user_role"] = Akismet.get_user_roles(comment["user_ID"])
        # end if
        #// See filter documentation in init_hooks().
        akismet_nonce_option = apply_filters("akismet_comment_nonce", get_option("akismet_comment_nonce"))
        comment["akismet_comment_nonce"] = "inactive"
        if akismet_nonce_option == "true" or akismet_nonce_option == "":
            comment["akismet_comment_nonce"] = "failed"
            if (php_isset(lambda : PHP_POST["akismet_comment_nonce"])) and wp_verify_nonce(PHP_POST["akismet_comment_nonce"], "akismet_comment_nonce_" + comment["comment_post_ID"]):
                comment["akismet_comment_nonce"] = "passed"
            # end if
            #// comment reply in wp-admin
            if (php_isset(lambda : PHP_POST["_ajax_nonce-replyto-comment"])) and check_ajax_referer("replyto-comment", "_ajax_nonce-replyto-comment"):
                comment["akismet_comment_nonce"] = "passed"
            # end if
        # end if
        if self.is_test_mode():
            comment["is_test"] = "true"
        # end if
        for key,value in PHP_POST:
            if php_is_string(value):
                comment[str("POST_") + str(key)] = value
            # end if
        # end for
        for key,value in PHP_SERVER:
            if (not php_is_string(value)):
                continue
            # end if
            if php_preg_match("/^HTTP_COOKIE/", key):
                continue
            # end if
            #// Send any potentially useful $_SERVER vars, but avoid sending junk we don't need.
            if php_preg_match("/^(HTTP_|REMOTE_ADDR|REQUEST_URI|DOCUMENT_URI)/", key):
                comment[str(key)] = value
            # end if
        # end for
        post = get_post(comment["comment_post_ID"])
        if (not is_null(post)):
            #// $post can technically be null, although in the past, it's always been an indicator of another plugin interfering.
            comment["comment_post_modified_gmt"] = post.post_modified_gmt
        # end if
        response = self.http_post(Akismet.build_query(comment), "comment-check")
        do_action("akismet_comment_check_response", response)
        commentdata["comment_as_submitted"] = php_array_intersect_key(comment, self.comment_as_submitted_allowed_keys)
        commentdata["akismet_result"] = response[1]
        if (php_isset(lambda : response[0]["x-akismet-pro-tip"])):
            commentdata["akismet_pro_tip"] = response[0]["x-akismet-pro-tip"]
        # end if
        if (php_isset(lambda : response[0]["x-akismet-error"])):
            #// An error occurred that we anticipated (like a suspended key) and want the user to act on.
            #// Send to moderation.
            self.last_comment_result = "0"
        else:
            if "true" == response[1]:
                #// akismet_spam_count will be incremented later by comment_is_spam()
                self.last_comment_result = "spam"
                discard = (php_isset(lambda : commentdata["akismet_pro_tip"])) and commentdata["akismet_pro_tip"] == "discard" and self.allow_discard()
                do_action("akismet_spam_caught", discard)
                if discard:
                    #// The spam is obvious, so we're bailing out early.
                    #// akismet_result_spam() won't be called so bump the counter here
                    incr = apply_filters("akismet_spam_count_incr", 1)
                    if incr:
                        update_option("akismet_spam_count", get_option("akismet_spam_count") + incr)
                    # end if
                    if self.is_rest_api_call:
                        return php_new_class("WP_Error", lambda : WP_Error("akismet_rest_comment_discarded", __("Comment discarded.", "akismet")))
                    else:
                        #// Redirect back to the previous page, or failing that, the post permalink, or failing that, the homepage of the blog.
                        redirect_to = PHP_SERVER["HTTP_REFERER"] if (php_isset(lambda : PHP_SERVER["HTTP_REFERER"])) else get_permalink(post) if post else home_url()
                        wp_safe_redirect(esc_url_raw(redirect_to))
                        php_exit(0)
                    # end if
                else:
                    if self.is_rest_api_call:
                        #// The way the REST API structures its calls, we can set the comment_approved value right away.
                        commentdata["comment_approved"] = "spam"
                    # end if
                # end if
            # end if
        # end if
        #// if the response is neither true nor false, hold the comment for moderation and schedule a recheck
        if "true" != response[1] and "false" != response[1]:
            if (not current_user_can("moderate_comments")):
                #// Comment status should be moderated
                self.last_comment_result = "0"
            # end if
            if (not wp_next_scheduled("akismet_schedule_cron_recheck")):
                wp_schedule_single_event(time() + 1200, "akismet_schedule_cron_recheck")
                do_action("akismet_scheduled_recheck", "invalid-response-" + response[1])
            # end if
            self.prevent_moderation_email_for_these_comments[-1] = commentdata
        # end if
        #// Delete old comments daily
        if (not wp_next_scheduled("akismet_scheduled_delete")):
            wp_schedule_event(time(), "daily", "akismet_scheduled_delete")
        # end if
        self.set_last_comment(commentdata)
        self.fix_scheduled_recheck()
        return commentdata
    # end def auto_check_comment
    @classmethod
    def get_last_comment(self):
        
        return self.last_comment
    # end def get_last_comment
    @classmethod
    def set_last_comment(self, comment=None):
        
        if is_null(comment):
            self.last_comment = None
        else:
            #// We filter it here so that it matches the filtered comment data that we'll have to compare against later.
            #// wp_filter_comment expects comment_author_IP
            self.last_comment = wp_filter_comment(php_array_merge(Array({"comment_author_IP": self.get_ip_address()}), comment))
        # end if
    # end def set_last_comment
    #// this fires on wp_insert_comment.  we can't update comment_meta when auto_check_comment() runs
    #// because we don't know the comment ID at that point.
    @classmethod
    def auto_check_update_meta(self, id=None, comment=None):
        
        #// wp_insert_comment() might be called in other contexts, so make sure this is the same comment
        #// as was checked by auto_check_comment
        if php_is_object(comment) and (not php_empty(lambda : self.last_comment)) and php_is_array(self.last_comment):
            if self.matches_last_comment(comment):
                load_plugin_textdomain("akismet")
                #// normal result: true or false
                if self.last_comment["akismet_result"] == "true":
                    update_comment_meta(comment.comment_ID, "akismet_result", "true")
                    self.update_comment_history(comment.comment_ID, "", "check-spam")
                    if comment.comment_approved != "spam":
                        self.update_comment_history(comment.comment_ID, "", "status-changed-" + comment.comment_approved)
                    # end if
                elif self.last_comment["akismet_result"] == "false":
                    update_comment_meta(comment.comment_ID, "akismet_result", "false")
                    self.update_comment_history(comment.comment_ID, "", "check-ham")
                    #// Status could be spam or trash, depending on the WP version and whether this change applies:
                    #// https://core.trac.wordpress.org/changeset/34726
                    if comment.comment_approved == "spam" or comment.comment_approved == "trash":
                        if wp_blacklist_check(comment.comment_author, comment.comment_author_email, comment.comment_author_url, comment.comment_content, comment.comment_author_IP, comment.comment_agent):
                            self.update_comment_history(comment.comment_ID, "", "wp-blacklisted")
                        else:
                            self.update_comment_history(comment.comment_ID, "", "status-changed-" + comment.comment_approved)
                        # end if
                    # end if
                else:
                    update_comment_meta(comment.comment_ID, "akismet_error", time())
                    self.update_comment_history(comment.comment_ID, "", "check-error", Array({"response": php_substr(self.last_comment["akismet_result"], 0, 50)}))
                # end if
                #// record the complete original data as submitted for checking
                if (php_isset(lambda : self.last_comment["comment_as_submitted"])):
                    update_comment_meta(comment.comment_ID, "akismet_as_submitted", self.last_comment["comment_as_submitted"])
                # end if
                if (php_isset(lambda : self.last_comment["akismet_pro_tip"])):
                    update_comment_meta(comment.comment_ID, "akismet_pro_tip", self.last_comment["akismet_pro_tip"])
                # end if
            # end if
        # end if
    # end def auto_check_update_meta
    @classmethod
    def delete_old_comments(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// 
        #// Determines how many comments will be deleted in each batch.
        #// 
        #// @param int The default, as defined by AKISMET_DELETE_LIMIT.
        #//
        delete_limit = apply_filters("akismet_delete_comment_limit", AKISMET_DELETE_LIMIT if php_defined("AKISMET_DELETE_LIMIT") else 10000)
        delete_limit = php_max(1, php_intval(delete_limit))
        #// 
        #// Determines how many days a comment will be left in the Spam queue before being deleted.
        #// 
        #// @param int The default number of days.
        #//
        delete_interval = apply_filters("akismet_delete_comment_interval", 15)
        delete_interval = php_max(1, php_intval(delete_interval))
        while True:
            comment_ids = wpdb.get_col(wpdb.prepare(str("SELECT comment_id FROM ") + str(wpdb.comments) + str(" WHERE DATE_SUB(NOW(), INTERVAL %d DAY) > comment_date_gmt AND comment_approved = 'spam' LIMIT %d"), delete_interval, delete_limit))
            if not (comment_ids):
                break
            # end if
            if php_empty(lambda : comment_ids):
                return
            # end if
            wpdb.queries = Array()
            for comment_id in comment_ids:
                do_action("delete_comment", comment_id)
                do_action("akismet_batch_delete_count", __FUNCTION__)
            # end for
            #// Prepared as strings since comment_id is an unsigned BIGINT, and using %d will constrain the value to the maximum signed BIGINT.
            format_string = php_implode(", ", array_fill(0, php_count(comment_ids), "%s"))
            wpdb.query(wpdb.prepare(str("DELETE FROM ") + str(wpdb.comments) + str(" WHERE comment_id IN ( ") + format_string + " )", comment_ids))
            wpdb.query(wpdb.prepare(str("DELETE FROM ") + str(wpdb.commentmeta) + str(" WHERE comment_id IN ( ") + format_string + " )", comment_ids))
            clean_comment_cache(comment_ids)
            do_action("akismet_delete_comment_batch", php_count(comment_ids))
        # end while
        if apply_filters("akismet_optimize_table", mt_rand(1, 5000) == 11, wpdb.comments):
            #// lucky number
            wpdb.query(str("OPTIMIZE TABLE ") + str(wpdb.comments))
        # end if
    # end def delete_old_comments
    @classmethod
    def delete_old_comments_meta(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        interval = apply_filters("akismet_delete_commentmeta_interval", 15)
        #// # enforce a minimum of 1 day
        interval = absint(interval)
        if interval < 1:
            interval = 1
        # end if
        #// akismet_as_submitted meta values are large, so expire them
        #// after $interval days regardless of the comment status
        while True:
            comment_ids = wpdb.get_col(wpdb.prepare(str("SELECT m.comment_id FROM ") + str(wpdb.commentmeta) + str(" as m INNER JOIN ") + str(wpdb.comments) + str(" as c USING(comment_id) WHERE m.meta_key = 'akismet_as_submitted' AND DATE_SUB(NOW(), INTERVAL %d DAY) > c.comment_date_gmt LIMIT 10000"), interval))
            if not (comment_ids):
                break
            # end if
            if php_empty(lambda : comment_ids):
                return
            # end if
            wpdb.queries = Array()
            for comment_id in comment_ids:
                delete_comment_meta(comment_id, "akismet_as_submitted")
                do_action("akismet_batch_delete_count", __FUNCTION__)
            # end for
            do_action("akismet_delete_commentmeta_batch", php_count(comment_ids))
        # end while
        if apply_filters("akismet_optimize_table", mt_rand(1, 5000) == 11, wpdb.commentmeta):
            #// lucky number
            wpdb.query(str("OPTIMIZE TABLE ") + str(wpdb.commentmeta))
        # end if
    # end def delete_old_comments_meta
    #// Clear out comments meta that no longer have corresponding comments in the database
    @classmethod
    def delete_orphaned_commentmeta(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        last_meta_id = 0
        start_time = PHP_SERVER["REQUEST_TIME_FLOAT"] if (php_isset(lambda : PHP_SERVER["REQUEST_TIME_FLOAT"])) else php_microtime(True)
        max_exec_time = php_max(php_ini_get("max_execution_time") - 5, 3)
        while True:
            commentmeta_results = wpdb.get_results(wpdb.prepare(str("SELECT m.meta_id, m.comment_id, m.meta_key FROM ") + str(wpdb.commentmeta) + str(" as m LEFT JOIN ") + str(wpdb.comments) + str(" as c USING(comment_id) WHERE c.comment_id IS NULL AND m.meta_id > %d ORDER BY m.meta_id LIMIT 1000"), last_meta_id))
            if not (commentmeta_results):
                break
            # end if
            if php_empty(lambda : commentmeta_results):
                return
            # end if
            wpdb.queries = Array()
            commentmeta_deleted = 0
            for commentmeta in commentmeta_results:
                if "akismet_" == php_substr(commentmeta.meta_key, 0, 8):
                    delete_comment_meta(commentmeta.comment_id, commentmeta.meta_key)
                    do_action("akismet_batch_delete_count", __FUNCTION__)
                    commentmeta_deleted += 1
                # end if
                last_meta_id = commentmeta.meta_id
            # end for
            do_action("akismet_delete_commentmeta_batch", commentmeta_deleted)
            #// If we're getting close to max_execution_time, quit for this round.
            if php_microtime(True) - start_time > max_exec_time:
                return
            # end if
        # end while
        if apply_filters("akismet_optimize_table", mt_rand(1, 5000) == 11, wpdb.commentmeta):
            #// lucky number
            wpdb.query(str("OPTIMIZE TABLE ") + str(wpdb.commentmeta))
        # end if
    # end def delete_orphaned_commentmeta
    #// how many approved comments does this author have?
    @classmethod
    def get_user_comments_approved(self, user_id=None, comment_author_email=None, comment_author=None, comment_author_url=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        if (not php_empty(lambda : user_id)):
            return php_int(wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.comments) + str(" WHERE user_id = %d AND comment_approved = 1"), user_id)))
        # end if
        if (not php_empty(lambda : comment_author_email)):
            return php_int(wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.comments) + str(" WHERE comment_author_email = %s AND comment_author = %s AND comment_author_url = %s AND comment_approved = 1"), comment_author_email, comment_author, comment_author_url)))
        # end if
        return 0
    # end def get_user_comments_approved
    #// get the full comment history for a given comment, as an array in reverse chronological order
    @classmethod
    def get_comment_history(self, comment_id=None):
        
        history = get_comment_meta(comment_id, "akismet_history", False)
        if php_empty(lambda : history) or php_empty(lambda : history[0]):
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
        usort(history, Array("Akismet", "_cmp_time"))
        return history
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
    def update_comment_history(self, comment_id=None, message=None, event=None, meta=None):
        
        global current_user
        php_check_if_defined("current_user")
        user = ""
        event = Array({"time": self._get_microtime(), "event": event})
        if php_is_object(current_user) and (php_isset(lambda : current_user.user_login)):
            event["user"] = current_user.user_login
        # end if
        if (not php_empty(lambda : meta)):
            event["meta"] = meta
        # end if
        #// $unique = false so as to allow multiple values per comment
        r = add_comment_meta(comment_id, "akismet_history", event, False)
    # end def update_comment_history
    @classmethod
    def check_db_comment(self, id=None, recheck_reason="recheck_queue"):
        
        global wpdb
        php_check_if_defined("wpdb")
        if (not self.get_api_key()):
            return php_new_class("WP_Error", lambda : WP_Error("akismet-not-configured", __("Akismet is not configured. Please enter an API key.", "akismet")))
        # end if
        c = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.comments) + str(" WHERE comment_ID = %d"), id), ARRAY_A)
        if (not c):
            return php_new_class("WP_Error", lambda : WP_Error("invalid-comment-id", __("Comment not found.", "akismet")))
        # end if
        c["user_ip"] = c["comment_author_IP"]
        c["user_agent"] = c["comment_agent"]
        c["referrer"] = ""
        c["blog"] = get_option("home")
        c["blog_lang"] = get_locale()
        c["blog_charset"] = get_option("blog_charset")
        c["permalink"] = get_permalink(c["comment_post_ID"])
        c["recheck_reason"] = recheck_reason
        c["user_role"] = ""
        if (not php_empty(lambda : c["user_ID"])):
            c["user_role"] = Akismet.get_user_roles(c["user_ID"])
        # end if
        if self.is_test_mode():
            c["is_test"] = "true"
        # end if
        response = self.http_post(Akismet.build_query(c), "comment-check")
        if (not php_empty(lambda : response[1])):
            return response[1]
        # end if
        return False
    # end def check_db_comment
    @classmethod
    def recheck_comment(self, id=None, recheck_reason="recheck_queue"):
        
        add_comment_meta(id, "akismet_rechecking", True)
        api_response = self.check_db_comment(id, recheck_reason)
        delete_comment_meta(id, "akismet_rechecking")
        if is_wp_error(api_response):
            pass
        else:
            if "true" == api_response:
                wp_set_comment_status(id, "spam")
                update_comment_meta(id, "akismet_result", "true")
                delete_comment_meta(id, "akismet_error")
                delete_comment_meta(id, "akismet_delayed_moderation_email")
                Akismet.update_comment_history(id, "", "recheck-spam")
            elif "false" == api_response:
                update_comment_meta(id, "akismet_result", "false")
                delete_comment_meta(id, "akismet_error")
                delete_comment_meta(id, "akismet_delayed_moderation_email")
                Akismet.update_comment_history(id, "", "recheck-ham")
            else:
                #// abnormal result: error
                update_comment_meta(id, "akismet_result", "error")
                Akismet.update_comment_history(id, "", "recheck-error", Array({"response": php_substr(api_response, 0, 50)}))
            # end if
        # end if
        return api_response
    # end def recheck_comment
    @classmethod
    def transition_comment_status(self, new_status=None, old_status=None, comment=None):
        
        if new_status == old_status:
            return
        # end if
        if "spam" == new_status or "spam" == old_status:
            #// Clear the cache of the "X comments in your spam queue" count on the dashboard.
            wp_cache_delete("akismet_spam_count", "widget")
        # end if
        #// # we don't need to record a history item for deleted comments
        if new_status == "delete":
            return
        # end if
        if (not current_user_can("edit_post", comment.comment_post_ID)) and (not current_user_can("moderate_comments")):
            return
        # end if
        if php_defined("WP_IMPORTING") and WP_IMPORTING == True:
            return
        # end if
        #// if this is present, it means the status has been changed by a re-check, not an explicit user action
        if get_comment_meta(comment.comment_ID, "akismet_rechecking"):
            return
        # end if
        #// Assumption alert:
        #// We want to submit comments to Akismet only when a moderator explicitly spams or approves it - not if the status
        #// is changed automatically by another plugin.  Unfortunately WordPress doesn't provide an unambiguous way to
        #// determine why the transition_comment_status action was triggered.  And there are several different ways by which
        #// to spam and unspam comments: bulk actions, ajax, links in moderation emails, the dashboard, and perhaps others.
        #// We'll assume that this is an explicit user action if certain POST/GET variables exist.
        if (php_isset(lambda : PHP_POST["status"])) and php_in_array(PHP_POST["status"], Array("spam", "unspam", "approved")) or (php_isset(lambda : PHP_POST["spam"])) and php_int(PHP_POST["spam"]) == 1 or (php_isset(lambda : PHP_POST["unspam"])) and php_int(PHP_POST["unspam"]) == 1 or (php_isset(lambda : PHP_POST["comment_status"])) and php_in_array(PHP_POST["comment_status"], Array("spam", "unspam")) or (php_isset(lambda : PHP_REQUEST["action"])) and php_in_array(PHP_REQUEST["action"], Array("spam", "unspam", "spamcomment", "unspamcomment")) or (php_isset(lambda : PHP_POST["action"])) and php_in_array(PHP_POST["action"], Array("editedcomment")) or (php_isset(lambda : PHP_REQUEST["for"])) and "jetpack" == PHP_REQUEST["for"] and (not php_defined("IS_WPCOM")) or (not IS_WPCOM) or php_defined("REST_API_REQUEST") and REST_API_REQUEST or php_defined("REST_REQUEST") and REST_REQUEST:
            if new_status == "spam" and old_status == "approved" or old_status == "unapproved" or (not old_status):
                return self.submit_spam_comment(comment.comment_ID)
            elif old_status == "spam" and new_status == "approved" or new_status == "unapproved":
                return self.submit_nonspam_comment(comment.comment_ID)
            # end if
        # end if
        self.update_comment_history(comment.comment_ID, "", "status-" + new_status)
    # end def transition_comment_status
    @classmethod
    def submit_spam_comment(self, comment_id=None):
        
        global wpdb,current_user,current_site
        php_check_if_defined("wpdb","current_user","current_site")
        comment_id = php_int(comment_id)
        comment = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.comments) + str(" WHERE comment_ID = %d"), comment_id))
        if (not comment):
            #// it was deleted
            return
        # end if
        if "spam" != comment.comment_approved:
            return
        # end if
        self.update_comment_history(comment_id, "", "report-spam")
        #// If the user hasn't configured Akismet, there's nothing else to do at this point.
        if (not self.get_api_key()):
            return
        # end if
        #// use the original version stored in comment_meta if available
        as_submitted = self.sanitize_comment_as_submitted(get_comment_meta(comment_id, "akismet_as_submitted", True))
        if as_submitted and php_is_array(as_submitted) and (php_isset(lambda : as_submitted["comment_content"])):
            comment = php_array_merge(comment, as_submitted)
        # end if
        comment.blog = get_option("home")
        comment.blog_lang = get_locale()
        comment.blog_charset = get_option("blog_charset")
        comment.permalink = get_permalink(comment.comment_post_ID)
        if php_is_object(current_user):
            comment.reporter = current_user.user_login
        # end if
        if php_is_object(current_site):
            comment.site_domain = current_site.domain
        # end if
        comment.user_role = ""
        if (not php_empty(lambda : comment.user_ID)):
            comment.user_role = Akismet.get_user_roles(comment.user_ID)
        # end if
        if self.is_test_mode():
            comment.is_test = "true"
        # end if
        post = get_post(comment.comment_post_ID)
        if (not is_null(post)):
            comment.comment_post_modified_gmt = post.post_modified_gmt
        # end if
        response = Akismet.http_post(Akismet.build_query(comment), "submit-spam")
        update_comment_meta(comment_id, "akismet_user_result", "true")
        if comment.reporter:
            update_comment_meta(comment_id, "akismet_user", comment.reporter)
        # end if
        do_action("akismet_submit_spam_comment", comment_id, response[1])
    # end def submit_spam_comment
    @classmethod
    def submit_nonspam_comment(self, comment_id=None):
        
        global wpdb,current_user,current_site
        php_check_if_defined("wpdb","current_user","current_site")
        comment_id = php_int(comment_id)
        comment = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.comments) + str(" WHERE comment_ID = %d"), comment_id))
        if (not comment):
            #// it was deleted
            return
        # end if
        self.update_comment_history(comment_id, "", "report-ham")
        #// If the user hasn't configured Akismet, there's nothing else to do at this point.
        if (not self.get_api_key()):
            return
        # end if
        #// use the original version stored in comment_meta if available
        as_submitted = self.sanitize_comment_as_submitted(get_comment_meta(comment_id, "akismet_as_submitted", True))
        if as_submitted and php_is_array(as_submitted) and (php_isset(lambda : as_submitted["comment_content"])):
            comment = php_array_merge(comment, as_submitted)
        # end if
        comment.blog = get_option("home")
        comment.blog_lang = get_locale()
        comment.blog_charset = get_option("blog_charset")
        comment.permalink = get_permalink(comment.comment_post_ID)
        comment.user_role = ""
        if php_is_object(current_user):
            comment.reporter = current_user.user_login
        # end if
        if php_is_object(current_site):
            comment.site_domain = current_site.domain
        # end if
        if (not php_empty(lambda : comment.user_ID)):
            comment.user_role = Akismet.get_user_roles(comment.user_ID)
        # end if
        if Akismet.is_test_mode():
            comment.is_test = "true"
        # end if
        post = get_post(comment.comment_post_ID)
        if (not is_null(post)):
            comment.comment_post_modified_gmt = post.post_modified_gmt
        # end if
        response = self.http_post(Akismet.build_query(comment), "submit-ham")
        update_comment_meta(comment_id, "akismet_user_result", "false")
        if comment.reporter:
            update_comment_meta(comment_id, "akismet_user", comment.reporter)
        # end if
        do_action("akismet_submit_nonspam_comment", comment_id, response[1])
    # end def submit_nonspam_comment
    @classmethod
    def cron_recheck(self):
        
        global wpdb
        php_check_if_defined("wpdb")
        api_key = self.get_api_key()
        status = self.verify_key(api_key)
        if get_option("akismet_alert_code") or status == "invalid":
            #// since there is currently a problem with the key, reschedule a check for 6 hours hence
            wp_schedule_single_event(time() + 21600, "akismet_schedule_cron_recheck")
            do_action("akismet_scheduled_recheck", "key-problem-" + get_option("akismet_alert_code") + "-" + status)
            return False
        # end if
        delete_option("akismet_available_servers")
        comment_errors = wpdb.get_col(str("SELECT comment_id FROM ") + str(wpdb.commentmeta) + str(" WHERE meta_key = 'akismet_error'   LIMIT 100"))
        load_plugin_textdomain("akismet")
        for comment_id in comment_errors:
            #// if the comment no longer exists, or is too old, remove the meta entry from the queue to avoid getting stuck
            comment = get_comment(comment_id)
            if (not comment) or strtotime(comment.comment_date_gmt) < strtotime("-15 days") or comment.comment_approved != "0":
                delete_comment_meta(comment_id, "akismet_error")
                delete_comment_meta(comment_id, "akismet_delayed_moderation_email")
                continue
            # end if
            add_comment_meta(comment_id, "akismet_rechecking", True)
            status = self.check_db_comment(comment_id, "retry")
            event = ""
            if status == "true":
                event = "cron-retry-spam"
            elif status == "false":
                event = "cron-retry-ham"
            # end if
            #// If we got back a legit response then update the comment history
            #// other wise just bail now and try again later.  No point in
            #// re-trying all the comments once we hit one failure.
            if (not php_empty(lambda : event)):
                delete_comment_meta(comment_id, "akismet_error")
                self.update_comment_history(comment_id, "", event)
                update_comment_meta(comment_id, "akismet_result", status)
                #// make sure the comment status is still pending.  if it isn't, that means the user has already moved it elsewhere.
                comment = get_comment(comment_id)
                if comment and "unapproved" == wp_get_comment_status(comment_id):
                    if status == "true":
                        wp_spam_comment(comment_id)
                    elif status == "false":
                        #// comment is good, but it's still in the pending queue.  depending on the moderation settings
                        #// we may need to change it to approved.
                        if check_comment(comment.comment_author, comment.comment_author_email, comment.comment_author_url, comment.comment_content, comment.comment_author_IP, comment.comment_agent, comment.comment_type):
                            wp_set_comment_status(comment_id, 1)
                        else:
                            if get_comment_meta(comment_id, "akismet_delayed_moderation_email", True):
                                wp_notify_moderator(comment_id)
                            # end if
                        # end if
                    # end if
                # end if
                delete_comment_meta(comment_id, "akismet_delayed_moderation_email")
            else:
                #// If this comment has been pending moderation for longer than MAX_DELAY_BEFORE_MODERATION_EMAIL,
                #// send a moderation email now.
                if php_intval(gmdate("U")) - strtotime(comment.comment_date_gmt) < self.MAX_DELAY_BEFORE_MODERATION_EMAIL:
                    delete_comment_meta(comment_id, "akismet_delayed_moderation_email")
                    wp_notify_moderator(comment_id)
                # end if
                delete_comment_meta(comment_id, "akismet_rechecking")
                wp_schedule_single_event(time() + 1200, "akismet_schedule_cron_recheck")
                do_action("akismet_scheduled_recheck", "check-db-comment-" + status)
                return
            # end if
            delete_comment_meta(comment_id, "akismet_rechecking")
        # end for
        remaining = wpdb.get_var(str("SELECT COUNT(*) FROM ") + str(wpdb.commentmeta) + str(" WHERE meta_key = 'akismet_error'"))
        if remaining and (not wp_next_scheduled("akismet_schedule_cron_recheck")):
            wp_schedule_single_event(time() + 1200, "akismet_schedule_cron_recheck")
            do_action("akismet_scheduled_recheck", "remaining")
        # end if
    # end def cron_recheck
    @classmethod
    def fix_scheduled_recheck(self):
        
        future_check = wp_next_scheduled("akismet_schedule_cron_recheck")
        if (not future_check):
            return
        # end if
        if get_option("akismet_alert_code") > 0:
            return
        # end if
        check_range = time() + 1200
        if future_check > check_range:
            wp_clear_scheduled_hook("akismet_schedule_cron_recheck")
            wp_schedule_single_event(time() + 300, "akismet_schedule_cron_recheck")
            do_action("akismet_scheduled_recheck", "fix-scheduled-recheck")
        # end if
    # end def fix_scheduled_recheck
    @classmethod
    def add_comment_nonce(self, post_id=None):
        
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
        akismet_comment_nonce_option = apply_filters("akismet_comment_nonce", get_option("akismet_comment_nonce"))
        if akismet_comment_nonce_option == "true" or akismet_comment_nonce_option == "":
            php_print("<p style=\"display: none;\">")
            wp_nonce_field("akismet_comment_nonce_" + post_id, "akismet_comment_nonce", False)
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
    def comments_match(self, comment1=None, comment2=None):
        
        comment1 = comment1
        comment2 = comment2
        #// Set default values for these strings that we check in order to simplify
        #// the checks and avoid PHP warnings.
        if (not (php_isset(lambda : comment1["comment_author"]))):
            comment1["comment_author"] = ""
        # end if
        if (not (php_isset(lambda : comment2["comment_author"]))):
            comment2["comment_author"] = ""
        # end if
        if (not (php_isset(lambda : comment1["comment_author_email"]))):
            comment1["comment_author_email"] = ""
        # end if
        if (not (php_isset(lambda : comment2["comment_author_email"]))):
            comment2["comment_author_email"] = ""
        # end if
        comments_match = (php_isset(lambda : comment1["comment_post_ID"]) and php_isset(lambda : comment2["comment_post_ID"])) and php_intval(comment1["comment_post_ID"]) == php_intval(comment2["comment_post_ID"]) and php_substr(comment1["comment_author"], 0, 248) == php_substr(comment2["comment_author"], 0, 248) or php_substr(stripslashes(comment1["comment_author"]), 0, 248) == php_substr(comment2["comment_author"], 0, 248) or php_substr(comment1["comment_author"], 0, 248) == php_substr(stripslashes(comment2["comment_author"]), 0, 248) or (not comment1["comment_author"]) and php_strlen(comment2["comment_author"]) > 248 or (not comment2["comment_author"]) and php_strlen(comment1["comment_author"]) > 248 and php_substr(comment1["comment_author_email"], 0, 93) == php_substr(comment2["comment_author_email"], 0, 93) or php_substr(stripslashes(comment1["comment_author_email"]), 0, 93) == php_substr(comment2["comment_author_email"], 0, 93) or php_substr(comment1["comment_author_email"], 0, 93) == php_substr(stripslashes(comment2["comment_author_email"]), 0, 93) or (not comment1["comment_author_email"]) and php_strlen(comment2["comment_author_email"]) > 100 or (not comment2["comment_author_email"]) and php_strlen(comment1["comment_author_email"]) > 100
        return comments_match
    # end def comments_match
    #// Does the supplied comment match the details of the one most recently stored in self::$last_comment?
    @classmethod
    def matches_last_comment(self, comment=None):
        
        return self.comments_match(self.last_comment, comment)
    # end def matches_last_comment
    def get_user_agent(self):
        
        return PHP_SERVER["HTTP_USER_AGENT"] if (php_isset(lambda : PHP_SERVER["HTTP_USER_AGENT"])) else None
    # end def get_user_agent
    def get_referer(self):
        
        return PHP_SERVER["HTTP_REFERER"] if (php_isset(lambda : PHP_SERVER["HTTP_REFERER"])) else None
    # end def get_referer
    #// return a comma-separated list of role names for the given user
    @classmethod
    def get_user_roles(self, user_id=None):
        
        roles = False
        if (not php_class_exists("WP_User")):
            return False
        # end if
        if user_id > 0:
            comment_user = php_new_class("WP_User", lambda : WP_User(user_id))
            if (php_isset(lambda : comment_user.roles)):
                roles = join(",", comment_user.roles)
            # end if
        # end if
        if is_multisite() and is_super_admin(user_id):
            if php_empty(lambda : roles):
                roles = "super_admin"
            else:
                comment_user.roles[-1] = "super_admin"
                roles = join(",", comment_user.roles)
            # end if
        # end if
        return roles
    # end def get_user_roles
    #// filter handler used to return a spam result to pre_comment_approved
    @classmethod
    def last_comment_status(self, approved=None, comment=None):
        
        if is_null(self.last_comment_result):
            #// We didn't have reason to store the result of the last check.
            return approved
        # end if
        #// Only do this if it's the correct comment
        if (not self.matches_last_comment(comment)):
            self.log(str("comment_is_spam mismatched comment, returning unaltered ") + str(approved))
            return approved
        # end if
        if "trash" == approved:
            #// If the last comment we checked has had its approval set to 'trash',
            #// then it failed the comment blacklist check. Let that blacklist override
            #// the spam check, since users have the (valid) expectation that when
            #// they fill out their blacklists, comments that match it will always
            #// end up in the trash.
            return approved
        # end if
        #// bump the counter here instead of when the filter is added to reduce the possibility of overcounting
        incr = apply_filters("akismet_spam_count_incr", 1)
        if incr:
            update_option("akismet_spam_count", get_option("akismet_spam_count") + incr)
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
    def disable_moderation_emails_if_unreachable(self, emails=None, comment_id=None):
        
        if (not php_empty(lambda : self.prevent_moderation_email_for_these_comments)) and (not php_empty(lambda : emails)):
            comment = get_comment(comment_id)
            for possible_match in self.prevent_moderation_email_for_these_comments:
                if self.comments_match(possible_match, comment):
                    update_comment_meta(comment_id, "akismet_delayed_moderation_email", True)
                    return Array()
                # end if
            # end for
        # end if
        return emails
    # end def disable_moderation_emails_if_unreachable
    @classmethod
    def _cmp_time(self, a=None, b=None):
        
        return -1 if a["time"] > b["time"] else 1
    # end def _cmp_time
    @classmethod
    def _get_microtime(self):
        
        mtime = php_explode(" ", php_microtime())
        return mtime[1] + mtime[0]
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
    def http_post(self, request=None, path=None, ip=None):
        
        akismet_ua = php_sprintf("WordPress/%s | Akismet/%s", PHP_GLOBALS["wp_version"], constant("AKISMET_VERSION"))
        akismet_ua = apply_filters("akismet_ua", akismet_ua)
        content_length = php_strlen(request)
        api_key = self.get_api_key()
        host = self.API_HOST
        if (not php_empty(lambda : api_key)):
            host = api_key + "." + host
        # end if
        http_host = host
        #// use a specific IP if provided
        #// needed by Akismet_Admin::check_server_connectivity()
        if ip and long2ip(ip2long(ip)):
            http_host = ip
        # end if
        http_args = Array({"body": request, "headers": Array({"Content-Type": "application/x-www-form-urlencoded; charset=" + get_option("blog_charset"), "Host": host, "User-Agent": akismet_ua})}, {"httpversion": "1.0", "timeout": 15})
        akismet_url = http_akismet_url = str("http://") + str(http_host) + str("/1.1/") + str(path)
        #// 
        #// Try SSL first; if that fails, try without it and don't try it again for a while.
        #//
        ssl = ssl_failed = False
        #// Check if SSL requests were disabled fewer than X hours ago.
        ssl_disabled = get_option("akismet_ssl_disabled")
        if ssl_disabled and ssl_disabled < time() - 60 * 60 * 24:
            #// 24 hours
            ssl_disabled = False
            delete_option("akismet_ssl_disabled")
        else:
            if ssl_disabled:
                do_action("akismet_ssl_disabled")
            # end if
        # end if
        ssl = wp_http_supports(Array("ssl"))
        if (not ssl_disabled) and ssl:
            akismet_url = set_url_scheme(akismet_url, "https")
            do_action("akismet_https_request_pre")
        # end if
        response = wp_remote_post(akismet_url, http_args)
        Akismet.log(compact("akismet_url", "http_args", "response"))
        if ssl and is_wp_error(response):
            do_action("akismet_https_request_failure", response)
            #// Intermittent connection problems may cause the first HTTPS
            #// request to fail and subsequent HTTP requests to succeed randomly.
            #// Retry the HTTPS request once before disabling SSL for a time.
            response = wp_remote_post(akismet_url, http_args)
            Akismet.log(compact("akismet_url", "http_args", "response"))
            if is_wp_error(response):
                ssl_failed = True
                do_action("akismet_https_request_failure", response)
                do_action("akismet_http_request_pre")
                #// Try the request again without SSL.
                response = wp_remote_post(http_akismet_url, http_args)
                Akismet.log(compact("http_akismet_url", "http_args", "response"))
            # end if
        # end if
        if is_wp_error(response):
            do_action("akismet_request_failure", response)
            return Array("", "")
        # end if
        if ssl_failed:
            #// The request failed when using SSL but succeeded without it. Disable SSL for future requests.
            update_option("akismet_ssl_disabled", time())
            do_action("akismet_https_disabled")
        # end if
        simplified_response = Array(response["headers"], response["body"])
        self.update_alert(simplified_response)
        return simplified_response
    # end def http_post
    #// given a response from an API call like check_key_status(), update the alert code options if an alert is present.
    @classmethod
    def update_alert(self, response=None):
        
        code = msg = None
        if (php_isset(lambda : response[0]["x-akismet-alert-code"])):
            code = response[0]["x-akismet-alert-code"]
            msg = response[0]["x-akismet-alert-msg"]
        # end if
        #// only call update_option() if the value has changed
        if code != get_option("akismet_alert_code"):
            if (not code):
                delete_option("akismet_alert_code")
                delete_option("akismet_alert_msg")
            else:
                update_option("akismet_alert_code", code)
                update_option("akismet_alert_msg", msg)
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
    def set_form_js_async(self, tag=None, handle=None, src=None):
        
        if "akismet-form" != handle:
            return tag
        # end if
        return php_preg_replace("/^<script /i", "<script async=\"async\" ", tag)
    # end def set_form_js_async
    @classmethod
    def inject_ak_js(self, fields=None):
        
        php_print("<p style=\"display: none;\">")
        php_print("<input type=\"hidden\" id=\"ak_js\" name=\"ak_js\" value=\"" + mt_rand(0, 250) + "\"/>")
        php_print("</p>")
    # end def inject_ak_js
    def bail_on_activation(self, message=None, deactivate=True):
        
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
        php_print(esc_html(message))
        php_print("""</p>
        </body>
        </html>
        """)
        if deactivate:
            plugins = get_option("active_plugins")
            akismet = plugin_basename(AKISMET__PLUGIN_DIR + "akismet.php")
            update = False
            for i,plugin in plugins:
                if plugin == akismet:
                    plugins[i] = False
                    update = True
                # end if
            # end for
            if update:
                update_option("active_plugins", php_array_filter(plugins))
            # end if
        # end if
        php_exit(0)
    # end def bail_on_activation
    @classmethod
    def view(self, name=None, args=Array()):
        
        args = apply_filters("akismet_view_arguments", args, name)
        for key,val in args:
            key = val
        # end for
        load_plugin_textdomain("akismet")
        file = AKISMET__PLUGIN_DIR + "views/" + name + ".php"
        php_include_file(file, once=False)
    # end def view
    #// 
    #// Attached to activate_{ plugin_basename( __FILES__ ) } by register_activation_hook()
    #// @static
    #//
    @classmethod
    def plugin_activation(self):
        
        if php_version_compare(PHP_GLOBALS["wp_version"], AKISMET__MINIMUM_WP_VERSION, "<"):
            load_plugin_textdomain("akismet")
            message = "<strong>" + php_sprintf(esc_html__("Akismet %s requires WordPress %s or higher.", "akismet"), AKISMET_VERSION, AKISMET__MINIMUM_WP_VERSION) + "</strong> " + php_sprintf(__("Please <a href=\"%1$s\">upgrade WordPress</a> to a current version, or <a href=\"%2$s\">downgrade to version 2.4 of the Akismet plugin</a>.", "akismet"), "https://codex.wordpress.org/Upgrading_WordPress", "https://wordpress.org/extend/plugins/akismet/download/")
            Akismet.bail_on_activation(message)
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
        akismet_cron_events = Array("akismet_schedule_cron_recheck", "akismet_scheduled_delete")
        for akismet_cron_event in akismet_cron_events:
            timestamp = wp_next_scheduled(akismet_cron_event)
            if timestamp:
                wp_unschedule_event(timestamp, akismet_cron_event)
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
    def build_query(self, args=None):
        
        return _http_build_query(args, "", "&")
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
    def log(self, akismet_debug=None):
        
        if apply_filters("akismet_debug_log", php_defined("WP_DEBUG") and WP_DEBUG and php_defined("WP_DEBUG_LOG") and WP_DEBUG_LOG and php_defined("AKISMET_DEBUG") and AKISMET_DEBUG):
            php_error_log(print_r(compact("akismet_debug"), True))
        # end if
    # end def log
    @classmethod
    def pre_check_pingback(self, method=None):
        
        if method != "pingback.ping":
            return
        # end if
        global wp_xmlrpc_server
        php_check_if_defined("wp_xmlrpc_server")
        if (not php_is_object(wp_xmlrpc_server)):
            return False
        # end if
        #// Lame: tightly coupled with the IXR class.
        args = wp_xmlrpc_server.message.params
        if (not php_empty(lambda : args[1])):
            post_id = url_to_postid(args[1])
            #// If pingbacks aren't open on this post, we'll still check whether this request is part of a potential DDOS,
            #// but indicate to the server that pingbacks are indeed closed so we don't include this request in the user's stats,
            #// since the user has already done their part by disabling pingbacks.
            pingbacks_closed = False
            post = get_post(post_id)
            if (not post) or (not pings_open(post)):
                pingbacks_closed = True
            # end if
            comment = Array({"comment_author_url": args[0], "comment_post_ID": post_id, "comment_author": "", "comment_author_email": "", "comment_content": "", "comment_type": "pingback", "akismet_pre_check": "1", "comment_pingback_target": args[1], "pingbacks_closed": "1" if pingbacks_closed else "0"})
            comment = Akismet.auto_check_comment(comment)
            if (php_isset(lambda : comment["akismet_result"])) and "true" == comment["akismet_result"]:
                #// Lame: tightly coupled with the IXR classes. Unfortunately the action provides no context and no way to return anything.
                wp_xmlrpc_server.error(php_new_class("IXR_Error", lambda : IXR_Error(0, "Invalid discovery target")))
            # end if
        # end if
    # end def pre_check_pingback
    #// 
    #// Ensure that we are loading expected scalar values from akismet_as_submitted commentmeta.
    #// 
    #// @param mixed $meta_value
    #// @return mixed
    #//
    def sanitize_comment_as_submitted(self, meta_value=None):
        
        if php_empty(lambda : meta_value):
            return meta_value
        # end if
        meta_value = meta_value
        for key,value in meta_value:
            if (not (php_isset(lambda : self.comment_as_submitted_allowed_keys[key]))) or (not is_scalar(value)):
                meta_value[key] = None
            # end if
        # end for
        return meta_value
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
