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
#// WP_Importer base class
#//
class WP_Importer():
    #// 
    #// Class Constructor
    #//
    def __init__(self):
        
        
        pass
    # end def __init__
    #// 
    #// Returns array with imported permalinks from WordPress database
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $importer_name
    #// @param string $bid
    #// @return array
    #//
    def get_imported_posts(self, importer_name_=None, bid_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        hashtable_ = Array()
        limit_ = 100
        offset_ = 0
        #// Grab all posts in chunks.
        while True:
            meta_key_ = importer_name_ + "_" + bid_ + "_permalink"
            sql_ = wpdb_.prepare(str("SELECT post_id, meta_value FROM ") + str(wpdb_.postmeta) + str(" WHERE meta_key = %s LIMIT %d,%d"), meta_key_, offset_, limit_)
            results_ = wpdb_.get_results(sql_)
            #// Increment offset.
            offset_ = limit_ + offset_
            if (not php_empty(lambda : results_)):
                for r_ in results_:
                    #// Set permalinks into array.
                    hashtable_[r_.meta_value] = php_intval(r_.post_id)
                # end for
            # end if
            
            if php_count(results_) == limit_:
                break
            # end if
        # end while
        results_ = None
        r_ = None
        return hashtable_
    # end def get_imported_posts
    #// 
    #// Return count of imported permalinks from WordPress database
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $importer_name
    #// @param string $bid
    #// @return int
    #//
    def count_imported_posts(self, importer_name_=None, bid_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        count_ = 0
        #// Get count of permalinks.
        meta_key_ = importer_name_ + "_" + bid_ + "_permalink"
        sql_ = wpdb_.prepare(str("SELECT COUNT( post_id ) AS cnt FROM ") + str(wpdb_.postmeta) + str(" WHERE meta_key = %s"), meta_key_)
        result_ = wpdb_.get_results(sql_)
        if (not php_empty(lambda : result_)):
            count_ = php_intval(result_[0].cnt)
        # end if
        results_ = None
        return count_
    # end def count_imported_posts
    #// 
    #// Set array with imported comments from WordPress database
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $bid
    #// @return array
    #//
    def get_imported_comments(self, bid_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        hashtable_ = Array()
        limit_ = 100
        offset_ = 0
        #// Grab all comments in chunks.
        while True:
            sql_ = wpdb_.prepare(str("SELECT comment_ID, comment_agent FROM ") + str(wpdb_.comments) + str(" LIMIT %d,%d"), offset_, limit_)
            results_ = wpdb_.get_results(sql_)
            #// Increment offset.
            offset_ = limit_ + offset_
            if (not php_empty(lambda : results_)):
                for r_ in results_:
                    #// Explode comment_agent key.
                    ca_bid_, source_comment_id_ = php_explode("-", r_.comment_agent)
                    source_comment_id_ = php_intval(source_comment_id_)
                    #// Check if this comment came from this blog.
                    if bid_ == ca_bid_:
                        hashtable_[source_comment_id_] = php_intval(r_.comment_ID)
                    # end if
                # end for
            # end if
            
            if php_count(results_) == limit_:
                break
            # end if
        # end while
        results_ = None
        r_ = None
        return hashtable_
    # end def get_imported_comments
    #// 
    #// @param int $blog_id
    #// @return int|void
    #//
    def set_blog(self, blog_id_=None):
        
        
        if php_is_numeric(blog_id_):
            blog_id_ = php_int(blog_id_)
        else:
            blog_ = "http://" + php_preg_replace("#^https?://#", "", blog_id_)
            parsed_ = php_parse_url(blog_)
            if (not parsed_) or php_empty(lambda : parsed_["host"]):
                fwrite(STDERR, str("Error: can not determine blog_id from ") + str(blog_id_) + str("\n"))
                php_exit(0)
            # end if
            if php_empty(lambda : parsed_["path"]):
                parsed_["path"] = "/"
            # end if
            blogs_ = get_sites(Array({"domain": parsed_["host"], "number": 1, "path": parsed_["path"]}))
            if (not blogs_):
                fwrite(STDERR, "Error: Could not find blog\n")
                php_exit(0)
            # end if
            blog_ = php_array_shift(blogs_)
            blog_id_ = php_int(blog_.blog_id)
        # end if
        if php_function_exists("is_multisite"):
            if is_multisite():
                switch_to_blog(blog_id_)
            # end if
        # end if
        return blog_id_
    # end def set_blog
    #// 
    #// @param int $user_id
    #// @return int|void
    #//
    def set_user(self, user_id_=None):
        
        
        if php_is_numeric(user_id_):
            user_id_ = php_int(user_id_)
        else:
            user_id_ = php_int(username_exists(user_id_))
        # end if
        if (not user_id_) or (not wp_set_current_user(user_id_)):
            fwrite(STDERR, "Error: can not find user\n")
            php_exit(0)
        # end if
        return user_id_
    # end def set_user
    #// 
    #// Sort by strlen, longest string first
    #// 
    #// @param string $a
    #// @param string $b
    #// @return int
    #//
    def cmpr_strlen(self, a_=None, b_=None):
        
        
        return php_strlen(b_) - php_strlen(a_)
    # end def cmpr_strlen
    #// 
    #// GET URL
    #// 
    #// @param string $url
    #// @param string $username
    #// @param string $password
    #// @param bool   $head
    #// @return array
    #//
    def get_page(self, url_=None, username_="", password_="", head_=None):
        if head_ is None:
            head_ = False
        # end if
        
        #// Increase the timeout.
        add_filter("http_request_timeout", Array(self, "bump_request_timeout"))
        headers_ = Array()
        args_ = Array()
        if True == head_:
            args_["method"] = "HEAD"
        # end if
        if (not php_empty(lambda : username_)) and (not php_empty(lambda : password_)):
            headers_["Authorization"] = "Basic " + php_base64_encode(str(username_) + str(":") + str(password_))
        # end if
        args_["headers"] = headers_
        return wp_safe_remote_request(url_, args_)
    # end def get_page
    #// 
    #// Bump up the request timeout for http requests
    #// 
    #// @param int $val
    #// @return int
    #//
    def bump_request_timeout(self, val_=None):
        
        
        return 60
    # end def bump_request_timeout
    #// 
    #// Check if user has exceeded disk quota
    #// 
    #// @return bool
    #//
    def is_user_over_quota(self):
        
        
        if php_function_exists("upload_is_user_over_quota"):
            if upload_is_user_over_quota():
                return True
            # end if
        # end if
        return False
    # end def is_user_over_quota
    #// 
    #// Replace newlines, tabs, and multiple spaces with a single space
    #// 
    #// @param string $string
    #// @return string
    #//
    def min_whitespace(self, string_=None):
        
        
        return php_preg_replace("|[\\r\\n\\t ]+|", " ", string_)
    # end def min_whitespace
    #// 
    #// Resets global variables that grow out of control during imports.
    #// 
    #// @since 3.0.0
    #// 
    #// @global wpdb  $wpdb       WordPress database abstraction object.
    #// @global array $wp_actions
    #//
    def stop_the_insanity(self):
        
        
        global wpdb_
        global wp_actions_
        php_check_if_defined("wpdb_","wp_actions_")
        #// Or define( 'WP_IMPORTING', true );
        wpdb_.queries = Array()
        #// Reset $wp_actions to keep it from growing out of control.
        wp_actions_ = Array()
    # end def stop_the_insanity
# end class WP_Importer
#// 
#// Returns value of command line params.
#// Exits when a required param is not set.
#// 
#// @param string $param
#// @param bool   $required
#// @return mixed
#//
def get_cli_args(param_=None, required_=None, *_args_):
    if required_ is None:
        required_ = False
    # end if
    
    args_ = PHP_SERVER["argv"]
    if (not php_is_array(args_)):
        args_ = Array()
    # end if
    out_ = Array()
    last_arg_ = None
    return_ = None
    il_ = sizeof(args_)
    i_ = 1
    il_
    while i_ < il_:
        
        if php_bool(php_preg_match("/^--(.+)/", args_[i_], match_)):
            parts_ = php_explode("=", match_[1])
            key_ = php_preg_replace("/[^a-z0-9]+/", "", parts_[0])
            if (php_isset(lambda : parts_[1])):
                out_[key_] = parts_[1]
            else:
                out_[key_] = True
            # end if
            last_arg_ = key_
        elif php_bool(php_preg_match("/^-([a-zA-Z0-9]+)/", args_[i_], match_)):
            j_ = 0
            jl_ = php_strlen(match_[1])
            while j_ < jl_:
                
                key_ = match_[1][j_]
                out_[key_] = True
                j_ += 1
            # end while
            last_arg_ = key_
        elif None != last_arg_:
            out_[last_arg_] = args_[i_]
        # end if
        i_ += 1
    # end while
    #// Check array for specified param.
    if (php_isset(lambda : out_[param_])):
        #// Set return value.
        return_ = out_[param_]
    # end if
    #// Check for missing required param.
    if (not (php_isset(lambda : out_[param_]))) and required_:
        #// Display message and exit.
        php_print(str("\"") + str(param_) + str("\" parameter is required but was not specified\n"))
        php_exit(0)
    # end if
    return return_
# end def get_cli_args
