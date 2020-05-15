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
    def get_imported_posts(self, importer_name=None, bid=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        hashtable = Array()
        limit = 100
        offset = 0
        #// Grab all posts in chunks.
        while True:
            meta_key = importer_name + "_" + bid + "_permalink"
            sql = wpdb.prepare(str("SELECT post_id, meta_value FROM ") + str(wpdb.postmeta) + str(" WHERE meta_key = %s LIMIT %d,%d"), meta_key, offset, limit)
            results = wpdb.get_results(sql)
            #// Increment offset.
            offset = limit + offset
            if (not php_empty(lambda : results)):
                for r in results:
                    #// Set permalinks into array.
                    hashtable[r.meta_value] = php_intval(r.post_id)
                # end for
            # end if
            
            if php_count(results) == limit:
                break
            # end if
        # end while
        results = None
        r = None
        return hashtable
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
    def count_imported_posts(self, importer_name=None, bid=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        count = 0
        #// Get count of permalinks.
        meta_key = importer_name + "_" + bid + "_permalink"
        sql = wpdb.prepare(str("SELECT COUNT( post_id ) AS cnt FROM ") + str(wpdb.postmeta) + str(" WHERE meta_key = %s"), meta_key)
        result = wpdb.get_results(sql)
        if (not php_empty(lambda : result)):
            count = php_intval(result[0].cnt)
        # end if
        results = None
        return count
    # end def count_imported_posts
    #// 
    #// Set array with imported comments from WordPress database
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $bid
    #// @return array
    #//
    def get_imported_comments(self, bid=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        hashtable = Array()
        limit = 100
        offset = 0
        #// Grab all comments in chunks.
        while True:
            sql = wpdb.prepare(str("SELECT comment_ID, comment_agent FROM ") + str(wpdb.comments) + str(" LIMIT %d,%d"), offset, limit)
            results = wpdb.get_results(sql)
            #// Increment offset.
            offset = limit + offset
            if (not php_empty(lambda : results)):
                for r in results:
                    #// Explode comment_agent key.
                    ca_bid, source_comment_id = php_explode("-", r.comment_agent)
                    source_comment_id = php_intval(source_comment_id)
                    #// Check if this comment came from this blog.
                    if bid == ca_bid:
                        hashtable[source_comment_id] = php_intval(r.comment_ID)
                    # end if
                # end for
            # end if
            
            if php_count(results) == limit:
                break
            # end if
        # end while
        results = None
        r = None
        return hashtable
    # end def get_imported_comments
    #// 
    #// @param int $blog_id
    #// @return int|void
    #//
    def set_blog(self, blog_id=None):
        
        if php_is_numeric(blog_id):
            blog_id = int(blog_id)
        else:
            blog = "http://" + php_preg_replace("#^https?://#", "", blog_id)
            parsed = php_parse_url(blog)
            if (not parsed) or php_empty(lambda : parsed["host"]):
                fwrite(STDERR, str("Error: can not determine blog_id from ") + str(blog_id) + str("\n"))
                php_exit(0)
            # end if
            if php_empty(lambda : parsed["path"]):
                parsed["path"] = "/"
            # end if
            blogs = get_sites(Array({"domain": parsed["host"], "number": 1, "path": parsed["path"]}))
            if (not blogs):
                fwrite(STDERR, "Error: Could not find blog\n")
                php_exit(0)
            # end if
            blog = php_array_shift(blogs)
            blog_id = int(blog.blog_id)
        # end if
        if php_function_exists("is_multisite"):
            if is_multisite():
                switch_to_blog(blog_id)
            # end if
        # end if
        return blog_id
    # end def set_blog
    #// 
    #// @param int $user_id
    #// @return int|void
    #//
    def set_user(self, user_id=None):
        
        if php_is_numeric(user_id):
            user_id = int(user_id)
        else:
            user_id = int(username_exists(user_id))
        # end if
        if (not user_id) or (not wp_set_current_user(user_id)):
            fwrite(STDERR, "Error: can not find user\n")
            php_exit(0)
        # end if
        return user_id
    # end def set_user
    #// 
    #// Sort by strlen, longest string first
    #// 
    #// @param string $a
    #// @param string $b
    #// @return int
    #//
    def cmpr_strlen(self, a=None, b=None):
        
        return php_strlen(b) - php_strlen(a)
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
    def get_page(self, url=None, username="", password="", head=False):
        
        #// Increase the timeout.
        add_filter("http_request_timeout", Array(self, "bump_request_timeout"))
        headers = Array()
        args = Array()
        if True == head:
            args["method"] = "HEAD"
        # end if
        if (not php_empty(lambda : username)) and (not php_empty(lambda : password)):
            headers["Authorization"] = "Basic " + php_base64_encode(str(username) + str(":") + str(password))
        # end if
        args["headers"] = headers
        return wp_safe_remote_request(url, args)
    # end def get_page
    #// 
    #// Bump up the request timeout for http requests
    #// 
    #// @param int $val
    #// @return int
    #//
    def bump_request_timeout(self, val=None):
        
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
    def min_whitespace(self, string=None):
        
        return php_preg_replace("|[\\r\\n\\t ]+|", " ", string)
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
        
        global wpdb,wp_actions
        php_check_if_defined("wpdb","wp_actions")
        #// Or define( 'WP_IMPORTING', true );
        wpdb.queries = Array()
        #// Reset $wp_actions to keep it from growing out of control.
        wp_actions = Array()
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
def get_cli_args(param=None, required=False, *args_):
    
    args = PHP_SERVER["argv"]
    if (not php_is_array(args)):
        args = Array()
    # end if
    out = Array()
    last_arg = None
    return_ = None
    il = sizeof(args)
    i = 1
    il
    while i < il:
        
        if bool(php_preg_match("/^--(.+)/", args[i], match)):
            parts = php_explode("=", match[1])
            key = php_preg_replace("/[^a-z0-9]+/", "", parts[0])
            if (php_isset(lambda : parts[1])):
                out[key] = parts[1]
            else:
                out[key] = True
            # end if
            last_arg = key
        elif bool(php_preg_match("/^-([a-zA-Z0-9]+)/", args[i], match)):
            j = 0
            jl = php_strlen(match[1])
            while j < jl:
                
                key = match[1][j]
                out[key] = True
                j += 1
            # end while
            last_arg = key
        elif None != last_arg:
            out[last_arg] = args[i]
        # end if
        i += 1
    # end while
    #// Check array for specified param.
    if (php_isset(lambda : out[param])):
        #// Set return value.
        return_ = out[param]
    # end if
    #// Check for missing required param.
    if (not (php_isset(lambda : out[param]))) and required:
        #// Display message and exit.
        php_print(str("\"") + str(param) + str("\" parameter is required but was not specified\n"))
        php_exit(0)
    # end if
    return return_
# end def get_cli_args
