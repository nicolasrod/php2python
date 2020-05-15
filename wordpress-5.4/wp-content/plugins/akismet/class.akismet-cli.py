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
    def check(self, args=None, assoc_args=None):
        
        for comment_id in args:
            if (php_isset(lambda : assoc_args["noaction"])):
                #// Check the comment, but don't reclassify it.
                api_response = Akismet.check_db_comment(comment_id, "wp-cli")
            else:
                api_response = Akismet.recheck_comment(comment_id, "wp-cli")
            # end if
            if "true" == api_response:
                WP_CLI.line(php_sprintf(__("Comment #%d is spam.", "akismet"), comment_id))
            else:
                if "false" == api_response:
                    WP_CLI.line(php_sprintf(__("Comment #%d is not spam.", "akismet"), comment_id))
                else:
                    if False == api_response:
                        WP_CLI.error(__("Failed to connect to Akismet.", "akismet"))
                    else:
                        if is_wp_error(api_response):
                            WP_CLI.warning(php_sprintf(__("Comment #%d could not be checked.", "akismet"), comment_id))
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
        
        batch_size = 100
        start = 0
        total_counts = Array()
        while True:
            result_counts = Akismet_Admin.recheck_queue_portion(start, batch_size)
            if result_counts["processed"] > 0:
                for key,count in result_counts:
                    if (not (php_isset(lambda : total_counts[key]))):
                        total_counts[key] = count
                    else:
                        total_counts[key] += count
                    # end if
                # end for
                start += batch_size
                start -= result_counts["spam"]
                pass
            # end if
            
            if result_counts["processed"] > 0:
                break
            # end if
        # end while
        WP_CLI.line(php_sprintf(_n("Processed %d comment.", "Processed %d comments.", total_counts["processed"], "akismet"), number_format(total_counts["processed"])))
        WP_CLI.line(php_sprintf(_n("%d comment moved to Spam.", "%d comments moved to Spam.", total_counts["spam"], "akismet"), number_format(total_counts["spam"])))
        if total_counts["error"]:
            WP_CLI.line(php_sprintf(_n("%d comment could not be checked.", "%d comments could not be checked.", total_counts["error"], "akismet"), number_format(total_counts["error"])))
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
    def stats(self, args=None, assoc_args=None):
        
        api_key = Akismet.get_api_key()
        if php_empty(lambda : api_key):
            WP_CLI.error(__("API key must be set to fetch stats.", "akismet"))
        # end if
        for case in Switch(args[0]):
            if case("days"):
                interval = "60-days"
                break
            # end if
            if case("months"):
                interval = "6-months"
                break
            # end if
            if case():
                interval = "all"
                break
            # end if
        # end for
        response = Akismet.http_post(Akismet.build_query(Array({"blog": get_option("home"), "key": api_key, "from": interval})), "get-stats")
        if php_empty(lambda : response[1]):
            WP_CLI.error(__("Currently unable to fetch stats. Please try again.", "akismet"))
        # end if
        response_body = php_json_decode(response[1], True)
        if php_is_null(response_body):
            WP_CLI.error(__("Stats response could not be decoded.", "akismet"))
        # end if
        if (php_isset(lambda : assoc_args["summary"])):
            keys = Array("spam", "ham", "missed_spam", "false_positives", "accuracy", "time_saved")
            WP_CLI.Utils.format_items(assoc_args["format"], Array(response_body), keys)
        else:
            stats = response_body["breakdown"]
            WP_CLI.Utils.format_items(assoc_args["format"], stats, php_array_keys(php_end(stats)))
        # end if
    # end def stats
# end class Akismet_CLI
