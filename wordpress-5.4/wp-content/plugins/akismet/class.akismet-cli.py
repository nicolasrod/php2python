#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
WP_CLI.add_command("akismet", "Akismet_CLI")
#// 
#// Filter spam comments.
#//
class Akismet_CLI(WP_CLI_Command):
    #// 
    #// Checks one or more comments against the Akismet API.
    #// 
    #// ## OPTIONS
    #// <comment_id>...
    #// : The ID(s) of the comment(s) to check.
    #// 
    #// [--noaction]
    #// : Don't change the status of the comment. Just report what Akismet thinks it is.
    #// 
    #// ## EXAMPLES
    #// 
    #// wp akismet check 12345
    #// 
    #// @alias comment-check
    #//
    def check(self, args_=None, assoc_args_=None):
        
        
        for comment_id_ in args_:
            if (php_isset(lambda : assoc_args_["noaction"])):
                #// Check the comment, but don't reclassify it.
                api_response_ = Akismet.check_db_comment(comment_id_, "wp-cli")
            else:
                api_response_ = Akismet.recheck_comment(comment_id_, "wp-cli")
            # end if
            if "true" == api_response_:
                WP_CLI.line(php_sprintf(__("Comment #%d is spam.", "akismet"), comment_id_))
            else:
                if "false" == api_response_:
                    WP_CLI.line(php_sprintf(__("Comment #%d is not spam.", "akismet"), comment_id_))
                else:
                    if False == api_response_:
                        WP_CLI.error(__("Failed to connect to Akismet.", "akismet"))
                    else:
                        if is_wp_error(api_response_):
                            WP_CLI.warning(php_sprintf(__("Comment #%d could not be checked.", "akismet"), comment_id_))
                        # end if
                    # end if
                # end if
            # end if
        # end for
    # end def check
    #// 
    #// Recheck all comments in the Pending queue.
    #// 
    #// ## EXAMPLES
    #// 
    #// wp akismet recheck_queue
    #// 
    #// @alias recheck-queue
    #//
    def recheck_queue(self):
        
        
        batch_size_ = 100
        start_ = 0
        total_counts_ = Array()
        while True:
            result_counts_ = Akismet_Admin.recheck_queue_portion(start_, batch_size_)
            if result_counts_["processed"] > 0:
                for key_,count_ in result_counts_:
                    if (not (php_isset(lambda : total_counts_[key_]))):
                        total_counts_[key_] = count_
                    else:
                        total_counts_[key_] += count_
                    # end if
                # end for
                start_ += batch_size_
                start_ -= result_counts_["spam"]
                pass
            # end if
            
            if result_counts_["processed"] > 0:
                break
            # end if
        # end while
        WP_CLI.line(php_sprintf(_n("Processed %d comment.", "Processed %d comments.", total_counts_["processed"], "akismet"), number_format(total_counts_["processed"])))
        WP_CLI.line(php_sprintf(_n("%d comment moved to Spam.", "%d comments moved to Spam.", total_counts_["spam"], "akismet"), number_format(total_counts_["spam"])))
        if total_counts_["error"]:
            WP_CLI.line(php_sprintf(_n("%d comment could not be checked.", "%d comments could not be checked.", total_counts_["error"], "akismet"), number_format(total_counts_["error"])))
        # end if
    # end def recheck_queue
    #// 
    #// Fetches stats from the Akismet API.
    #// 
    #// ## OPTIONS
    #// 
    #// [<interval>]
    #// : The time period for which to retrieve stats.
    #// ---
    #// default: all
    #// options:
    #// - days
    #// - months
    #// - all
    #// ---
    #// 
    #// [--format=<format>]
    #// : Allows overriding the output of the command when listing connections.
    #// ---
    #// default: table
    #// options:
    #// - table
    #// - json
    #// - csv
    #// - yaml
    #// - count
    #// ---
    #// 
    #// [--summary]
    #// : When set, will display a summary of the stats.
    #// 
    #// ## EXAMPLES
    #// 
    #// wp akismet stats
    #// wp akismet stats all
    #// wp akismet stats days
    #// wp akismet stats months
    #// wp akismet stats all --summary
    #//
    def stats(self, args_=None, assoc_args_=None):
        
        
        api_key_ = Akismet.get_api_key()
        if php_empty(lambda : api_key_):
            WP_CLI.error(__("API key must be set to fetch stats.", "akismet"))
        # end if
        for case in Switch(args_[0]):
            if case("days"):
                interval_ = "60-days"
                break
            # end if
            if case("months"):
                interval_ = "6-months"
                break
            # end if
            if case():
                interval_ = "all"
                break
            # end if
        # end for
        response_ = Akismet.http_post(Akismet.build_query(Array({"blog": get_option("home"), "key": api_key_, "from": interval_})), "get-stats")
        if php_empty(lambda : response_[1]):
            WP_CLI.error(__("Currently unable to fetch stats. Please try again.", "akismet"))
        # end if
        response_body_ = php_json_decode(response_[1], True)
        if is_null(response_body_):
            WP_CLI.error(__("Stats response could not be decoded.", "akismet"))
        # end if
        if (php_isset(lambda : assoc_args_["summary"])):
            keys_ = Array("spam", "ham", "missed_spam", "false_positives", "accuracy", "time_saved")
            WP_CLI.Utils.format_items(assoc_args_["format"], Array(response_body_), keys_)
        else:
            stats_ = response_body_["breakdown"]
            WP_CLI.Utils.format_items(assoc_args_["format"], stats_, php_array_keys(php_end(stats_)))
        # end if
    # end def stats
# end class Akismet_CLI
