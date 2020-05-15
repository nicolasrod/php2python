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
#// XML-RPC protocol support for WordPress
#// 
#// @package WordPress
#// @subpackage Publishing
#// 
#// 
#// WordPress XMLRPC server implementation.
#// 
#// Implements compatibility for Blogger API, MetaWeblog API, MovableType, and
#// pingback. Additional WordPress API for managing comments, pages, posts,
#// options, etc.
#// 
#// As of WordPress 3.5.0, XML-RPC is enabled by default. It can be disabled
#// via the {@see 'xmlrpc_enabled'} filter found in wp_xmlrpc_server::login().
#// 
#// @since 1.5.0
#// 
#// @see IXR_Server
#//
class wp_xmlrpc_server(IXR_Server):
    methods = Array()
    blog_options = Array()
    error = Array()
    auth_failed = False
    #// 
    #// Registers all of the XMLRPC methods that XMLRPC server understands.
    #// 
    #// Sets up server and method property. Passes XMLRPC
    #// methods through the {@see 'xmlrpc_methods'} filter to allow plugins to extend
    #// or replace XML-RPC methods.
    #// 
    #// @since 1.5.0
    #//
    def __init__(self):
        
        self.methods = Array({"wp.getUsersBlogs": "this:wp_getUsersBlogs", "wp.newPost": "this:wp_newPost", "wp.editPost": "this:wp_editPost", "wp.deletePost": "this:wp_deletePost", "wp.getPost": "this:wp_getPost", "wp.getPosts": "this:wp_getPosts", "wp.newTerm": "this:wp_newTerm", "wp.editTerm": "this:wp_editTerm", "wp.deleteTerm": "this:wp_deleteTerm", "wp.getTerm": "this:wp_getTerm", "wp.getTerms": "this:wp_getTerms", "wp.getTaxonomy": "this:wp_getTaxonomy", "wp.getTaxonomies": "this:wp_getTaxonomies", "wp.getUser": "this:wp_getUser", "wp.getUsers": "this:wp_getUsers", "wp.getProfile": "this:wp_getProfile", "wp.editProfile": "this:wp_editProfile", "wp.getPage": "this:wp_getPage", "wp.getPages": "this:wp_getPages", "wp.newPage": "this:wp_newPage", "wp.deletePage": "this:wp_deletePage", "wp.editPage": "this:wp_editPage", "wp.getPageList": "this:wp_getPageList", "wp.getAuthors": "this:wp_getAuthors", "wp.getCategories": "this:mw_getCategories", "wp.getTags": "this:wp_getTags", "wp.newCategory": "this:wp_newCategory", "wp.deleteCategory": "this:wp_deleteCategory", "wp.suggestCategories": "this:wp_suggestCategories", "wp.uploadFile": "this:mw_newMediaObject", "wp.deleteFile": "this:wp_deletePost", "wp.getCommentCount": "this:wp_getCommentCount", "wp.getPostStatusList": "this:wp_getPostStatusList", "wp.getPageStatusList": "this:wp_getPageStatusList", "wp.getPageTemplates": "this:wp_getPageTemplates", "wp.getOptions": "this:wp_getOptions", "wp.setOptions": "this:wp_setOptions", "wp.getComment": "this:wp_getComment", "wp.getComments": "this:wp_getComments", "wp.deleteComment": "this:wp_deleteComment", "wp.editComment": "this:wp_editComment", "wp.newComment": "this:wp_newComment", "wp.getCommentStatusList": "this:wp_getCommentStatusList", "wp.getMediaItem": "this:wp_getMediaItem", "wp.getMediaLibrary": "this:wp_getMediaLibrary", "wp.getPostFormats": "this:wp_getPostFormats", "wp.getPostType": "this:wp_getPostType", "wp.getPostTypes": "this:wp_getPostTypes", "wp.getRevisions": "this:wp_getRevisions", "wp.restoreRevision": "this:wp_restoreRevision", "blogger.getUsersBlogs": "this:blogger_getUsersBlogs", "blogger.getUserInfo": "this:blogger_getUserInfo", "blogger.getPost": "this:blogger_getPost", "blogger.getRecentPosts": "this:blogger_getRecentPosts", "blogger.newPost": "this:blogger_newPost", "blogger.editPost": "this:blogger_editPost", "blogger.deletePost": "this:blogger_deletePost", "metaWeblog.newPost": "this:mw_newPost", "metaWeblog.editPost": "this:mw_editPost", "metaWeblog.getPost": "this:mw_getPost", "metaWeblog.getRecentPosts": "this:mw_getRecentPosts", "metaWeblog.getCategories": "this:mw_getCategories", "metaWeblog.newMediaObject": "this:mw_newMediaObject", "metaWeblog.deletePost": "this:blogger_deletePost", "metaWeblog.getUsersBlogs": "this:blogger_getUsersBlogs", "mt.getCategoryList": "this:mt_getCategoryList", "mt.getRecentPostTitles": "this:mt_getRecentPostTitles", "mt.getPostCategories": "this:mt_getPostCategories", "mt.setPostCategories": "this:mt_setPostCategories", "mt.supportedMethods": "this:mt_supportedMethods", "mt.supportedTextFilters": "this:mt_supportedTextFilters", "mt.getTrackbackPings": "this:mt_getTrackbackPings", "mt.publishPost": "this:mt_publishPost", "pingback.ping": "this:pingback_ping", "pingback.extensions.getPingbacks": "this:pingback_extensions_getPingbacks", "demo.sayHello": "this:sayHello", "demo.addTwoNumbers": "this:addTwoNumbers"})
        self.initialise_blog_option_info()
        #// 
        #// Filters the methods exposed by the XML-RPC server.
        #// 
        #// This filter can be used to add new methods, and remove built-in methods.
        #// 
        #// @since 1.5.0
        #// 
        #// @param string[] $methods An array of XML-RPC methods, keyed by their methodName.
        #//
        self.methods = apply_filters("xmlrpc_methods", self.methods)
    # end def __init__
    #// 
    #// Make private/protected methods readable for backward compatibility.
    #// 
    #// @since 4.0.0
    #// 
    #// @param string   $name      Method to call.
    #// @param array    $arguments Arguments to pass when calling.
    #// @return array|IXR_Error|false Return value of the callback, false otherwise.
    #//
    def __call(self, name=None, arguments=None):
        
        if "_multisite_getUsersBlogs" == name:
            return self._multisite_getusersblogs(arguments)
        # end if
        return False
    # end def __call
    #// 
    #// Serves the XML-RPC request.
    #// 
    #// @since 2.9.0
    #//
    def serve_request(self):
        
        self.ixr_server(self.methods)
    # end def serve_request
    #// 
    #// Test XMLRPC API by saying, "Hello!" to client.
    #// 
    #// @since 1.5.0
    #// 
    #// @return string Hello string response.
    #//
    def sayhello(self):
        
        return "Hello!"
    # end def sayhello
    #// 
    #// Test XMLRPC API by adding two numbers for client.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int $number1 A number to add.
    #// @type int $number2 A second number to add.
    #// }
    #// @return int Sum of the two given numbers.
    #//
    def addtwonumbers(self, args=None):
        
        number1 = args[0]
        number2 = args[1]
        return number1 + number2
    # end def addtwonumbers
    #// 
    #// Log user in.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $username User's username.
    #// @param string $password User's password.
    #// @return WP_User|bool WP_User object if authentication passed, false otherwise
    #//
    def login(self, username=None, password=None):
        
        #// 
        #// Respect old get_option() filters left for back-compat when the 'enable_xmlrpc'
        #// option was deprecated in 3.5.0. Use the 'xmlrpc_enabled' hook instead.
        #//
        enabled = apply_filters("pre_option_enable_xmlrpc", False)
        if False == enabled:
            enabled = apply_filters("option_enable_xmlrpc", True)
        # end if
        #// 
        #// Filters whether XML-RPC methods requiring authentication are enabled.
        #// 
        #// Contrary to the way it's named, this filter does not control whether XML-RPC is *fully
        #// enabled, rather, it only controls whether XML-RPC methods requiring authentication - such
        #// as for publishing purposes - are enabled.
        #// 
        #// Further, the filter does not control whether pingbacks or other custom endpoints that don't
        #// require authentication are enabled. This behavior is expected, and due to how parity was matched
        #// with the `enable_xmlrpc` UI option the filter replaced when it was introduced in 3.5.
        #// 
        #// To disable XML-RPC methods that require authentication, use:
        #// 
        #// add_filter( 'xmlrpc_enabled', '__return_false' );
        #// 
        #// For more granular control over all XML-RPC methods and requests, see the {@see 'xmlrpc_methods'}
        #// and {@see 'xmlrpc_element_limit'} hooks.
        #// 
        #// @since 3.5.0
        #// 
        #// @param bool $enabled Whether XML-RPC is enabled. Default true.
        #//
        enabled = apply_filters("xmlrpc_enabled", enabled)
        if (not enabled):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(405, php_sprintf(__("XML-RPC services are disabled on this site."))))
            return False
        # end if
        if self.auth_failed:
            user = php_new_class("WP_Error", lambda : WP_Error("login_prevented"))
        else:
            user = wp_authenticate(username, password)
        # end if
        if is_wp_error(user):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(403, __("Incorrect username or password.")))
            #// Flag that authentication has failed once on this wp_xmlrpc_server instance.
            self.auth_failed = True
            #// 
            #// Filters the XML-RPC user login error message.
            #// 
            #// @since 3.5.0
            #// 
            #// @param string   $error The XML-RPC error message.
            #// @param WP_Error $user  WP_Error object.
            #//
            self.error = apply_filters("xmlrpc_login_error", self.error, user)
            return False
        # end if
        wp_set_current_user(user.ID)
        return user
    # end def login
    #// 
    #// Check user's credentials. Deprecated.
    #// 
    #// @since 1.5.0
    #// @deprecated 2.8.0 Use wp_xmlrpc_server::login()
    #// @see wp_xmlrpc_server::login()
    #// 
    #// @param string $username User's username.
    #// @param string $password User's password.
    #// @return bool Whether authentication passed.
    #//
    def login_pass_ok(self, username=None, password=None):
        
        return bool(self.login(username, password))
    # end def login_pass_ok
    #// 
    #// Escape string or array of strings for database.
    #// 
    #// @since 1.5.2
    #// 
    #// @param string|array $data Escape single string or array of strings.
    #// @return string|void Returns with string is passed, alters by-reference
    #// when array is passed.
    #//
    def escape(self, data=None):
        
        if (not php_is_array(data)):
            return wp_slash(data)
        # end if
        for v in data:
            if php_is_array(v):
                self.escape(v)
            elif (not php_is_object(v)):
                v = wp_slash(v)
            # end if
        # end for
    # end def escape
    #// 
    #// Retrieve custom fields for post.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int $post_id Post ID.
    #// @return array Custom fields, if exist.
    #//
    def get_custom_fields(self, post_id=None):
        
        post_id = int(post_id)
        custom_fields = Array()
        for meta in has_meta(post_id):
            #// Don't expose protected fields.
            if (not current_user_can("edit_post_meta", post_id, meta["meta_key"])):
                continue
            # end if
            custom_fields[-1] = Array({"id": meta["meta_id"], "key": meta["meta_key"], "value": meta["meta_value"]})
        # end for
        return custom_fields
    # end def get_custom_fields
    #// 
    #// Set custom fields for post.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int $post_id Post ID.
    #// @param array $fields Custom fields.
    #//
    def set_custom_fields(self, post_id=None, fields=None):
        
        post_id = int(post_id)
        for meta in fields:
            if (php_isset(lambda : meta["id"])):
                meta["id"] = int(meta["id"])
                pmeta = get_metadata_by_mid("post", meta["id"])
                if (not pmeta) or pmeta.post_id != post_id:
                    continue
                # end if
                if (php_isset(lambda : meta["key"])):
                    meta["key"] = wp_unslash(meta["key"])
                    if meta["key"] != pmeta.meta_key:
                        continue
                    # end if
                    meta["value"] = wp_unslash(meta["value"])
                    if current_user_can("edit_post_meta", post_id, meta["key"]):
                        update_metadata_by_mid("post", meta["id"], meta["value"])
                    # end if
                elif current_user_can("delete_post_meta", post_id, pmeta.meta_key):
                    delete_metadata_by_mid("post", meta["id"])
                # end if
            elif current_user_can("add_post_meta", post_id, wp_unslash(meta["key"])):
                add_post_meta(post_id, meta["key"], meta["value"])
            # end if
        # end for
    # end def set_custom_fields
    #// 
    #// Retrieve custom fields for a term.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $term_id Term ID.
    #// @return array Array of custom fields, if they exist.
    #//
    def get_term_custom_fields(self, term_id=None):
        
        term_id = int(term_id)
        custom_fields = Array()
        for meta in has_term_meta(term_id):
            if (not current_user_can("edit_term_meta", term_id)):
                continue
            # end if
            custom_fields[-1] = Array({"id": meta["meta_id"], "key": meta["meta_key"], "value": meta["meta_value"]})
        # end for
        return custom_fields
    # end def get_term_custom_fields
    #// 
    #// Set custom fields for a term.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $term_id Term ID.
    #// @param array $fields Custom fields.
    #//
    def set_term_custom_fields(self, term_id=None, fields=None):
        
        term_id = int(term_id)
        for meta in fields:
            if (php_isset(lambda : meta["id"])):
                meta["id"] = int(meta["id"])
                pmeta = get_metadata_by_mid("term", meta["id"])
                if (php_isset(lambda : meta["key"])):
                    meta["key"] = wp_unslash(meta["key"])
                    if meta["key"] != pmeta.meta_key:
                        continue
                    # end if
                    meta["value"] = wp_unslash(meta["value"])
                    if current_user_can("edit_term_meta", term_id):
                        update_metadata_by_mid("term", meta["id"], meta["value"])
                    # end if
                elif current_user_can("delete_term_meta", term_id):
                    delete_metadata_by_mid("term", meta["id"])
                # end if
            elif current_user_can("add_term_meta", term_id):
                add_term_meta(term_id, meta["key"], meta["value"])
            # end if
        # end for
    # end def set_term_custom_fields
    #// 
    #// Set up blog options property.
    #// 
    #// Passes property through {@see 'xmlrpc_blog_options'} filter.
    #// 
    #// @since 2.6.0
    #//
    def initialise_blog_option_info(self):
        
        self.blog_options = Array({"software_name": Array({"desc": __("Software Name"), "readonly": True, "value": "WordPress"})}, {"software_version": Array({"desc": __("Software Version"), "readonly": True, "value": get_bloginfo("version")})}, {"blog_url": Array({"desc": __("WordPress Address (URL)"), "readonly": True, "option": "siteurl"})}, {"home_url": Array({"desc": __("Site Address (URL)"), "readonly": True, "option": "home"})}, {"login_url": Array({"desc": __("Login Address (URL)"), "readonly": True, "value": wp_login_url()})}, {"admin_url": Array({"desc": __("The URL to the admin area"), "readonly": True, "value": get_admin_url()})}, {"image_default_link_type": Array({"desc": __("Image default link type"), "readonly": True, "option": "image_default_link_type"})}, {"image_default_size": Array({"desc": __("Image default size"), "readonly": True, "option": "image_default_size"})}, {"image_default_align": Array({"desc": __("Image default align"), "readonly": True, "option": "image_default_align"})}, {"template": Array({"desc": __("Template"), "readonly": True, "option": "template"})}, {"stylesheet": Array({"desc": __("Stylesheet"), "readonly": True, "option": "stylesheet"})}, {"post_thumbnail": Array({"desc": __("Post Thumbnail"), "readonly": True, "value": current_theme_supports("post-thumbnails")})}, {"time_zone": Array({"desc": __("Time Zone"), "readonly": False, "option": "gmt_offset"})}, {"blog_title": Array({"desc": __("Site Title"), "readonly": False, "option": "blogname"})}, {"blog_tagline": Array({"desc": __("Site Tagline"), "readonly": False, "option": "blogdescription"})}, {"date_format": Array({"desc": __("Date Format"), "readonly": False, "option": "date_format"})}, {"time_format": Array({"desc": __("Time Format"), "readonly": False, "option": "time_format"})}, {"users_can_register": Array({"desc": __("Allow new users to sign up"), "readonly": False, "option": "users_can_register"})}, {"thumbnail_size_w": Array({"desc": __("Thumbnail Width"), "readonly": False, "option": "thumbnail_size_w"})}, {"thumbnail_size_h": Array({"desc": __("Thumbnail Height"), "readonly": False, "option": "thumbnail_size_h"})}, {"thumbnail_crop": Array({"desc": __("Crop thumbnail to exact dimensions"), "readonly": False, "option": "thumbnail_crop"})}, {"medium_size_w": Array({"desc": __("Medium size image width"), "readonly": False, "option": "medium_size_w"})}, {"medium_size_h": Array({"desc": __("Medium size image height"), "readonly": False, "option": "medium_size_h"})}, {"medium_large_size_w": Array({"desc": __("Medium-Large size image width"), "readonly": False, "option": "medium_large_size_w"})}, {"medium_large_size_h": Array({"desc": __("Medium-Large size image height"), "readonly": False, "option": "medium_large_size_h"})}, {"large_size_w": Array({"desc": __("Large size image width"), "readonly": False, "option": "large_size_w"})}, {"large_size_h": Array({"desc": __("Large size image height"), "readonly": False, "option": "large_size_h"})}, {"default_comment_status": Array({"desc": __("Allow people to submit comments on new posts."), "readonly": False, "option": "default_comment_status"})}, {"default_ping_status": Array({"desc": __("Allow link notifications from other blogs (pingbacks and trackbacks) on new posts."), "readonly": False, "option": "default_ping_status"})})
        #// 
        #// Filters the XML-RPC blog options property.
        #// 
        #// @since 2.6.0
        #// 
        #// @param array $blog_options An array of XML-RPC blog options.
        #//
        self.blog_options = apply_filters("xmlrpc_blog_options", self.blog_options)
    # end def initialise_blog_option_info
    #// 
    #// Retrieve the blogs of the user.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type string $username Username.
    #// @type string $password Password.
    #// }
    #// @return array|IXR_Error Array contains:
    #// - 'isAdmin'
    #// - 'isPrimary' - whether the blog is the user's primary blog
    #// - 'url'
    #// - 'blogid'
    #// - 'blogName'
    #// - 'xmlrpc' - url of xmlrpc endpoint
    #//
    def wp_getusersblogs(self, args=None):
        
        if (not self.minimum_args(args, 2)):
            return self.error
        # end if
        #// If this isn't on WPMU then just use blogger_getUsersBlogs().
        if (not is_multisite()):
            array_unshift(args, 1)
            return self.blogger_getusersblogs(args)
        # end if
        self.escape(args)
        username = args[0]
        password = args[1]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// 
        #// Fires after the XML-RPC user has been authenticated but before the rest of
        #// the method logic begins.
        #// 
        #// All built-in XML-RPC methods use the action xmlrpc_call, with a parameter
        #// equal to the method's name, e.g., wp.getUsersBlogs, wp.newPost, etc.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string $name The method name.
        #//
        do_action("xmlrpc_call", "wp.getUsersBlogs")
        blogs = get_blogs_of_user(user.ID)
        struct = Array()
        primary_blog_id = 0
        active_blog = get_active_blog_for_user(user.ID)
        if active_blog:
            primary_blog_id = int(active_blog.blog_id)
        # end if
        for blog in blogs:
            #// Don't include blogs that aren't hosted at this site.
            if get_current_network_id() != blog.site_id:
                continue
            # end if
            blog_id = blog.userblog_id
            switch_to_blog(blog_id)
            is_admin = current_user_can("manage_options")
            is_primary = int(blog_id) == primary_blog_id
            struct[-1] = Array({"isAdmin": is_admin, "isPrimary": is_primary, "url": home_url("/"), "blogid": str(blog_id), "blogName": get_option("blogname"), "xmlrpc": site_url("xmlrpc.php", "rpc")})
            restore_current_blog()
        # end for
        return struct
    # end def wp_getusersblogs
    #// 
    #// Checks if the method received at least the minimum number of arguments.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $args  An array of arguments to check.
    #// @param int   $count Minimum number of arguments.
    #// @return bool True if `$args` contains at least `$count` arguments, false otherwise.
    #//
    def minimum_args(self, args=None, count=None):
        
        if (not php_is_array(args)) or php_count(args) < count:
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(400, __("Insufficient arguments passed to this XML-RPC method.")))
            return False
        # end if
        return True
    # end def minimum_args
    #// 
    #// Prepares taxonomy data for return in an XML-RPC object.
    #// 
    #// @param object $taxonomy The unprepared taxonomy data.
    #// @param array $fields    The subset of taxonomy fields to return.
    #// @return array The prepared taxonomy data.
    #//
    def _prepare_taxonomy(self, taxonomy=None, fields=None):
        
        _taxonomy = Array({"name": taxonomy.name, "label": taxonomy.label, "hierarchical": bool(taxonomy.hierarchical), "public": bool(taxonomy.public), "show_ui": bool(taxonomy.show_ui), "_builtin": bool(taxonomy._builtin)})
        if php_in_array("labels", fields):
            _taxonomy["labels"] = taxonomy.labels
        # end if
        if php_in_array("cap", fields):
            _taxonomy["cap"] = taxonomy.cap
        # end if
        if php_in_array("menu", fields):
            _taxonomy["show_in_menu"] = bool(_taxonomy.show_in_menu)
        # end if
        if php_in_array("object_type", fields):
            _taxonomy["object_type"] = array_unique(taxonomy.object_type)
        # end if
        #// 
        #// Filters XML-RPC-prepared data for the given taxonomy.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array       $_taxonomy An array of taxonomy data.
        #// @param WP_Taxonomy $taxonomy  Taxonomy object.
        #// @param array       $fields    The subset of taxonomy fields to return.
        #//
        return apply_filters("xmlrpc_prepare_taxonomy", _taxonomy, taxonomy, fields)
    # end def _prepare_taxonomy
    #// 
    #// Prepares term data for return in an XML-RPC object.
    #// 
    #// @param array|object $term The unprepared term data.
    #// @return array The prepared term data.
    #//
    def _prepare_term(self, term=None):
        
        _term = term
        if (not php_is_array(_term)):
            _term = get_object_vars(_term)
        # end if
        #// For integers which may be larger than XML-RPC supports ensure we return strings.
        _term["term_id"] = php_strval(_term["term_id"])
        _term["term_group"] = php_strval(_term["term_group"])
        _term["term_taxonomy_id"] = php_strval(_term["term_taxonomy_id"])
        _term["parent"] = php_strval(_term["parent"])
        #// Count we are happy to return as an integer because people really shouldn't use terms that much.
        _term["count"] = php_intval(_term["count"])
        #// Get term meta.
        _term["custom_fields"] = self.get_term_custom_fields(_term["term_id"])
        #// 
        #// Filters XML-RPC-prepared data for the given term.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array        $_term An array of term data.
        #// @param array|object $term  Term object or array.
        #//
        return apply_filters("xmlrpc_prepare_term", _term, term)
    # end def _prepare_term
    #// 
    #// Convert a WordPress date string to an IXR_Date object.
    #// 
    #// @param string $date Date string to convert.
    #// @return IXR_Date IXR_Date object.
    #//
    def _convert_date(self, date=None):
        
        if "0000-00-00 00:00:00" == date:
            return php_new_class("IXR_Date", lambda : IXR_Date("00000000T00:00:00Z"))
        # end if
        return php_new_class("IXR_Date", lambda : IXR_Date(mysql2date("Ymd\\TH:i:s", date, False)))
    # end def _convert_date
    #// 
    #// Convert a WordPress GMT date string to an IXR_Date object.
    #// 
    #// @param string $date_gmt WordPress GMT date string.
    #// @param string $date     Date string.
    #// @return IXR_Date IXR_Date object.
    #//
    def _convert_date_gmt(self, date_gmt=None, date=None):
        
        if "0000-00-00 00:00:00" != date and "0000-00-00 00:00:00" == date_gmt:
            return php_new_class("IXR_Date", lambda : IXR_Date(get_gmt_from_date(mysql2date("Y-m-d H:i:s", date, False), "Ymd\\TH:i:s")))
        # end if
        return self._convert_date(date_gmt)
    # end def _convert_date_gmt
    #// 
    #// Prepares post data for return in an XML-RPC object.
    #// 
    #// @param array $post   The unprepared post data.
    #// @param array $fields The subset of post type fields to return.
    #// @return array The prepared post data.
    #//
    def _prepare_post(self, post=None, fields=None):
        
        #// Holds the data for this post. built up based on $fields.
        _post = Array({"post_id": php_strval(post["ID"])})
        #// Prepare common post fields.
        post_fields = Array({"post_title": post["post_title"], "post_date": self._convert_date(post["post_date"]), "post_date_gmt": self._convert_date_gmt(post["post_date_gmt"], post["post_date"]), "post_modified": self._convert_date(post["post_modified"]), "post_modified_gmt": self._convert_date_gmt(post["post_modified_gmt"], post["post_modified"]), "post_status": post["post_status"], "post_type": post["post_type"], "post_name": post["post_name"], "post_author": post["post_author"], "post_password": post["post_password"], "post_excerpt": post["post_excerpt"], "post_content": post["post_content"], "post_parent": php_strval(post["post_parent"]), "post_mime_type": post["post_mime_type"], "link": get_permalink(post["ID"]), "guid": post["guid"], "menu_order": php_intval(post["menu_order"]), "comment_status": post["comment_status"], "ping_status": post["ping_status"], "sticky": "post" == post["post_type"] and is_sticky(post["ID"])})
        #// Thumbnail.
        post_fields["post_thumbnail"] = Array()
        thumbnail_id = get_post_thumbnail_id(post["ID"])
        if thumbnail_id:
            thumbnail_size = "post-thumbnail" if current_theme_supports("post-thumbnail") else "thumbnail"
            post_fields["post_thumbnail"] = self._prepare_media_item(get_post(thumbnail_id), thumbnail_size)
        # end if
        #// Consider future posts as published.
        if "future" == post_fields["post_status"]:
            post_fields["post_status"] = "publish"
        # end if
        #// Fill in blank post format.
        post_fields["post_format"] = get_post_format(post["ID"])
        if php_empty(lambda : post_fields["post_format"]):
            post_fields["post_format"] = "standard"
        # end if
        #// Merge requested $post_fields fields into $_post.
        if php_in_array("post", fields):
            _post = php_array_merge(_post, post_fields)
        else:
            requested_fields = php_array_intersect_key(post_fields, php_array_flip(fields))
            _post = php_array_merge(_post, requested_fields)
        # end if
        all_taxonomy_fields = php_in_array("taxonomies", fields)
        if all_taxonomy_fields or php_in_array("terms", fields):
            post_type_taxonomies = get_object_taxonomies(post["post_type"], "names")
            terms = wp_get_object_terms(post["ID"], post_type_taxonomies)
            _post["terms"] = Array()
            for term in terms:
                _post["terms"][-1] = self._prepare_term(term)
            # end for
        # end if
        if php_in_array("custom_fields", fields):
            _post["custom_fields"] = self.get_custom_fields(post["ID"])
        # end if
        if php_in_array("enclosure", fields):
            _post["enclosure"] = Array()
            enclosures = get_post_meta(post["ID"], "enclosure")
            if (not php_empty(lambda : enclosures)):
                encdata = php_explode("\n", enclosures[0])
                _post["enclosure"]["url"] = php_trim(htmlspecialchars(encdata[0]))
                _post["enclosure"]["length"] = int(php_trim(encdata[1]))
                _post["enclosure"]["type"] = php_trim(encdata[2])
            # end if
        # end if
        #// 
        #// Filters XML-RPC-prepared date for the given post.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array $_post  An array of modified post data.
        #// @param array $post   An array of post data.
        #// @param array $fields An array of post fields.
        #//
        return apply_filters("xmlrpc_prepare_post", _post, post, fields)
    # end def _prepare_post
    #// 
    #// Prepares post data for return in an XML-RPC object.
    #// 
    #// @since 3.4.0
    #// @since 4.6.0 Converted the `$post_type` parameter to accept a WP_Post_Type object.
    #// 
    #// @param WP_Post_Type $post_type Post type object.
    #// @param array        $fields    The subset of post fields to return.
    #// @return array The prepared post type data.
    #//
    def _prepare_post_type(self, post_type=None, fields=None):
        
        _post_type = Array({"name": post_type.name, "label": post_type.label, "hierarchical": bool(post_type.hierarchical), "public": bool(post_type.public), "show_ui": bool(post_type.show_ui), "_builtin": bool(post_type._builtin), "has_archive": bool(post_type.has_archive), "supports": get_all_post_type_supports(post_type.name)})
        if php_in_array("labels", fields):
            _post_type["labels"] = post_type.labels
        # end if
        if php_in_array("cap", fields):
            _post_type["cap"] = post_type.cap
            _post_type["map_meta_cap"] = bool(post_type.map_meta_cap)
        # end if
        if php_in_array("menu", fields):
            _post_type["menu_position"] = int(post_type.menu_position)
            _post_type["menu_icon"] = post_type.menu_icon
            _post_type["show_in_menu"] = bool(post_type.show_in_menu)
        # end if
        if php_in_array("taxonomies", fields):
            _post_type["taxonomies"] = get_object_taxonomies(post_type.name, "names")
        # end if
        #// 
        #// Filters XML-RPC-prepared date for the given post type.
        #// 
        #// @since 3.4.0
        #// @since 4.6.0 Converted the `$post_type` parameter to accept a WP_Post_Type object.
        #// 
        #// @param array        $_post_type An array of post type data.
        #// @param WP_Post_Type $post_type  Post type object.
        #//
        return apply_filters("xmlrpc_prepare_post_type", _post_type, post_type)
    # end def _prepare_post_type
    #// 
    #// Prepares media item data for return in an XML-RPC object.
    #// 
    #// @param object $media_item     The unprepared media item data.
    #// @param string $thumbnail_size The image size to use for the thumbnail URL.
    #// @return array The prepared media item data.
    #//
    def _prepare_media_item(self, media_item=None, thumbnail_size="thumbnail"):
        
        _media_item = Array({"attachment_id": php_strval(media_item.ID), "date_created_gmt": self._convert_date_gmt(media_item.post_date_gmt, media_item.post_date), "parent": media_item.post_parent, "link": wp_get_attachment_url(media_item.ID), "title": media_item.post_title, "caption": media_item.post_excerpt, "description": media_item.post_content, "metadata": wp_get_attachment_metadata(media_item.ID), "type": media_item.post_mime_type})
        thumbnail_src = image_downsize(media_item.ID, thumbnail_size)
        if thumbnail_src:
            _media_item["thumbnail"] = thumbnail_src[0]
        else:
            _media_item["thumbnail"] = _media_item["link"]
        # end if
        #// 
        #// Filters XML-RPC-prepared data for the given media item.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array  $_media_item    An array of media item data.
        #// @param object $media_item     Media item object.
        #// @param string $thumbnail_size Image size.
        #//
        return apply_filters("xmlrpc_prepare_media_item", _media_item, media_item, thumbnail_size)
    # end def _prepare_media_item
    #// 
    #// Prepares page data for return in an XML-RPC object.
    #// 
    #// @param object $page The unprepared page data.
    #// @return array The prepared page data.
    #//
    def _prepare_page(self, page=None):
        
        #// Get all of the page content and link.
        full_page = get_extended(page.post_content)
        link = get_permalink(page.ID)
        #// Get info the page parent if there is one.
        parent_title = ""
        if (not php_empty(lambda : page.post_parent)):
            parent = get_post(page.post_parent)
            parent_title = parent.post_title
        # end if
        #// Determine comment and ping settings.
        allow_comments = 1 if comments_open(page.ID) else 0
        allow_pings = 1 if pings_open(page.ID) else 0
        #// Format page date.
        page_date = self._convert_date(page.post_date)
        page_date_gmt = self._convert_date_gmt(page.post_date_gmt, page.post_date)
        #// Pull the categories info together.
        categories = Array()
        if is_object_in_taxonomy("page", "category"):
            for cat_id in wp_get_post_categories(page.ID):
                categories[-1] = get_cat_name(cat_id)
            # end for
        # end if
        #// Get the author info.
        author = get_userdata(page.post_author)
        page_template = get_page_template_slug(page.ID)
        if php_empty(lambda : page_template):
            page_template = "default"
        # end if
        _page = Array({"dateCreated": page_date, "userid": page.post_author, "page_id": page.ID, "page_status": page.post_status, "description": full_page["main"], "title": page.post_title, "link": link, "permaLink": link, "categories": categories, "excerpt": page.post_excerpt, "text_more": full_page["extended"], "mt_allow_comments": allow_comments, "mt_allow_pings": allow_pings, "wp_slug": page.post_name, "wp_password": page.post_password, "wp_author": author.display_name, "wp_page_parent_id": page.post_parent, "wp_page_parent_title": parent_title, "wp_page_order": page.menu_order, "wp_author_id": str(author.ID), "wp_author_display_name": author.display_name, "date_created_gmt": page_date_gmt, "custom_fields": self.get_custom_fields(page.ID), "wp_page_template": page_template})
        #// 
        #// Filters XML-RPC-prepared data for the given page.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array   $_page An array of page data.
        #// @param WP_Post $page  Page object.
        #//
        return apply_filters("xmlrpc_prepare_page", _page, page)
    # end def _prepare_page
    #// 
    #// Prepares comment data for return in an XML-RPC object.
    #// 
    #// @param object $comment The unprepared comment data.
    #// @return array The prepared comment data.
    #//
    def _prepare_comment(self, comment=None):
        
        #// Format page date.
        comment_date_gmt = self._convert_date_gmt(comment.comment_date_gmt, comment.comment_date)
        if "0" == comment.comment_approved:
            comment_status = "hold"
        elif "spam" == comment.comment_approved:
            comment_status = "spam"
        elif "1" == comment.comment_approved:
            comment_status = "approve"
        else:
            comment_status = comment.comment_approved
        # end if
        _comment = Array({"date_created_gmt": comment_date_gmt, "user_id": comment.user_id, "comment_id": comment.comment_ID, "parent": comment.comment_parent, "status": comment_status, "content": comment.comment_content, "link": get_comment_link(comment), "post_id": comment.comment_post_ID, "post_title": get_the_title(comment.comment_post_ID), "author": comment.comment_author, "author_url": comment.comment_author_url, "author_email": comment.comment_author_email, "author_ip": comment.comment_author_IP, "type": comment.comment_type})
        #// 
        #// Filters XML-RPC-prepared data for the given comment.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array      $_comment An array of prepared comment data.
        #// @param WP_Comment $comment  Comment object.
        #//
        return apply_filters("xmlrpc_prepare_comment", _comment, comment)
    # end def _prepare_comment
    #// 
    #// Prepares user data for return in an XML-RPC object.
    #// 
    #// @param WP_User $user   The unprepared user object.
    #// @param array   $fields The subset of user fields to return.
    #// @return array The prepared user data.
    #//
    def _prepare_user(self, user=None, fields=None):
        
        _user = Array({"user_id": php_strval(user.ID)})
        user_fields = Array({"username": user.user_login, "first_name": user.user_firstname, "last_name": user.user_lastname, "registered": self._convert_date(user.user_registered), "bio": user.user_description, "email": user.user_email, "nickname": user.nickname, "nicename": user.user_nicename, "url": user.user_url, "display_name": user.display_name, "roles": user.roles})
        if php_in_array("all", fields):
            _user = php_array_merge(_user, user_fields)
        else:
            if php_in_array("basic", fields):
                basic_fields = Array("username", "email", "registered", "display_name", "nicename")
                fields = php_array_merge(fields, basic_fields)
            # end if
            requested_fields = php_array_intersect_key(user_fields, php_array_flip(fields))
            _user = php_array_merge(_user, requested_fields)
        # end if
        #// 
        #// Filters XML-RPC-prepared data for the given user.
        #// 
        #// @since 3.5.0
        #// 
        #// @param array   $_user  An array of user data.
        #// @param WP_User $user   User object.
        #// @param array   $fields An array of user fields.
        #//
        return apply_filters("xmlrpc_prepare_user", _user, user, fields)
    # end def _prepare_user
    #// 
    #// Create a new post for any registered post type.
    #// 
    #// @since 3.4.0
    #// 
    #// @link https://en.wikipedia.org/wiki/RSS_enclosure for information on RSS enclosures.
    #// 
    #// @param array $args {
    #// Method arguments. Note: top-level arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id        Blog ID (unused).
    #// @type string $username       Username.
    #// @type string $password       Password.
    #// @type array  $content_struct {
    #// Content struct for adding a new post. See wp_insert_post() for information on
    #// additional post fields
    #// 
    #// @type string $post_type      Post type. Default 'post'.
    #// @type string $post_status    Post status. Default 'draft'
    #// @type string $post_title     Post title.
    #// @type int    $post_author    Post author ID.
    #// @type string $post_excerpt   Post excerpt.
    #// @type string $post_content   Post content.
    #// @type string $post_date_gmt  Post date in GMT.
    #// @type string $post_date      Post date.
    #// @type string $post_password  Post password (20-character limit).
    #// @type string $comment_status Post comment enabled status. Accepts 'open' or 'closed'.
    #// @type string $ping_status    Post ping status. Accepts 'open' or 'closed'.
    #// @type bool   $sticky         Whether the post should be sticky. Automatically false if
    #// `$post_status` is 'private'.
    #// @type int    $post_thumbnail ID of an image to use as the post thumbnail/featured image.
    #// @type array  $custom_fields  Array of meta key/value pairs to add to the post.
    #// @type array  $terms          Associative array with taxonomy names as keys and arrays
    #// of term IDs as values.
    #// @type array  $terms_names    Associative array with taxonomy names as keys and arrays
    #// of term names as values.
    #// @type array  $enclosure      {
    #// Array of feed enclosure data to add to post meta.
    #// 
    #// @type string $url    URL for the feed enclosure.
    #// @type int    $length Size in bytes of the enclosure.
    #// @type string $type   Mime-type for the enclosure.
    #// }
    #// }
    #// }
    #// @return int|IXR_Error Post ID on success, IXR_Error instance otherwise.
    #//
    def wp_newpost(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        content_struct = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// Convert the date field back to IXR form.
        if (php_isset(lambda : content_struct["post_date"])) and (not type(content_struct["post_date"]).__name__ == "IXR_Date"):
            content_struct["post_date"] = self._convert_date(content_struct["post_date"])
        # end if
        #// 
        #// Ignore the existing GMT date if it is empty or a non-GMT date was supplied in $content_struct,
        #// since _insert_post() will ignore the non-GMT date if the GMT date is set.
        #//
        if (php_isset(lambda : content_struct["post_date_gmt"])) and (not type(content_struct["post_date_gmt"]).__name__ == "IXR_Date"):
            if "0000-00-00 00:00:00" == content_struct["post_date_gmt"] or (php_isset(lambda : content_struct["post_date"])):
                content_struct["post_date_gmt"] = None
            else:
                content_struct["post_date_gmt"] = self._convert_date(content_struct["post_date_gmt"])
            # end if
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newPost")
        content_struct["ID"] = None
        return self._insert_post(user, content_struct)
    # end def wp_newpost
    #// 
    #// Helper method for filtering out elements from an array.
    #// 
    #// @since 3.4.0
    #// 
    #// @param int $count Number to compare to one.
    #//
    def _is_greater_than_one(self, count=None):
        
        return count > 1
    # end def _is_greater_than_one
    #// 
    #// Encapsulate the logic for sticking a post
    #// and determining if the user has permission to do so
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $post_data
    #// @param bool  $update
    #// @return void|IXR_Error
    #//
    def _toggle_sticky(self, post_data=None, update=False):
        
        post_type = get_post_type_object(post_data["post_type"])
        #// Private and password-protected posts cannot be stickied.
        if "private" == post_data["post_status"] or (not php_empty(lambda : post_data["post_password"])):
            #// Error if the client tried to stick the post, otherwise, silently unstick.
            if (not php_empty(lambda : post_data["sticky"])):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you cannot stick a private post.")))
            # end if
            if update:
                unstick_post(post_data["ID"])
            # end if
        elif (php_isset(lambda : post_data["sticky"])):
            if (not current_user_can(post_type.cap.edit_others_posts)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to make posts sticky.")))
            # end if
            sticky = wp_validate_boolean(post_data["sticky"])
            if sticky:
                stick_post(post_data["ID"])
            else:
                unstick_post(post_data["ID"])
            # end if
        # end if
    # end def _toggle_sticky
    #// 
    #// Helper method for wp_newPost() and wp_editPost(), containing shared logic.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_insert_post()
    #// 
    #// @param WP_User         $user           The post author if post_author isn't set in $content_struct.
    #// @param array|IXR_Error $content_struct Post data to insert.
    #// @return IXR_Error|string
    #//
    def _insert_post(self, user=None, content_struct=None):
        
        defaults = Array({"post_status": "draft", "post_type": "post", "post_author": None, "post_password": None, "post_excerpt": None, "post_content": None, "post_title": None, "post_date": None, "post_date_gmt": None, "post_format": None, "post_name": None, "post_thumbnail": None, "post_parent": None, "ping_status": None, "comment_status": None, "custom_fields": None, "terms_names": None, "terms": None, "sticky": None, "enclosure": None, "ID": None})
        post_data = wp_parse_args(php_array_intersect_key(content_struct, defaults), defaults)
        post_type = get_post_type_object(post_data["post_type"])
        if (not post_type):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid post type.")))
        # end if
        update = (not php_empty(lambda : post_data["ID"]))
        if update:
            if (not get_post(post_data["ID"])):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post ID.")))
            # end if
            if (not current_user_can("edit_post", post_data["ID"])):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
            # end if
            if get_post_type(post_data["ID"]) != post_data["post_type"]:
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("The post type may not be changed.")))
            # end if
        else:
            if (not current_user_can(post_type.cap.create_posts)) or (not current_user_can(post_type.cap.edit_posts)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to post on this site.")))
            # end if
        # end if
        for case in Switch(post_data["post_status"]):
            if case("draft"):
                pass
            # end if
            if case("pending"):
                break
            # end if
            if case("private"):
                if (not current_user_can(post_type.cap.publish_posts)):
                    return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create private posts in this post type.")))
                # end if
                break
            # end if
            if case("publish"):
                pass
            # end if
            if case("future"):
                if (not current_user_can(post_type.cap.publish_posts)):
                    return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish posts in this post type.")))
                # end if
                break
            # end if
            if case():
                if (not get_post_status_object(post_data["post_status"])):
                    post_data["post_status"] = "draft"
                # end if
                break
            # end if
        # end for
        if (not php_empty(lambda : post_data["post_password"])) and (not current_user_can(post_type.cap.publish_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create password protected posts in this post type.")))
        # end if
        post_data["post_author"] = absint(post_data["post_author"])
        if (not php_empty(lambda : post_data["post_author"])) and post_data["post_author"] != user.ID:
            if (not current_user_can(post_type.cap.edit_others_posts)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create posts as this user.")))
            # end if
            author = get_userdata(post_data["post_author"])
            if (not author):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid author ID.")))
            # end if
        else:
            post_data["post_author"] = user.ID
        # end if
        if (php_isset(lambda : post_data["comment_status"])) and "open" != post_data["comment_status"] and "closed" != post_data["comment_status"]:
            post_data["comment_status"] = None
        # end if
        if (php_isset(lambda : post_data["ping_status"])) and "open" != post_data["ping_status"] and "closed" != post_data["ping_status"]:
            post_data["ping_status"] = None
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : post_data["post_date_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated = php_rtrim(post_data["post_date_gmt"].getiso(), "Z") + "Z"
        elif (not php_empty(lambda : post_data["post_date"])):
            dateCreated = post_data["post_date"].getiso()
        # end if
        #// Default to not flagging the post date to be edited unless it's intentional.
        post_data["edit_date"] = False
        if (not php_empty(lambda : dateCreated)):
            post_data["post_date"] = iso8601_to_datetime(dateCreated)
            post_data["post_date_gmt"] = iso8601_to_datetime(dateCreated, "gmt")
            #// Flag the post date to be edited.
            post_data["edit_date"] = True
        # end if
        if (not (php_isset(lambda : post_data["ID"]))):
            post_data["ID"] = get_default_post_to_edit(post_data["post_type"], True).ID
        # end if
        post_ID = post_data["ID"]
        if "post" == post_data["post_type"]:
            error = self._toggle_sticky(post_data, update)
            if error:
                return error
            # end if
        # end if
        if (php_isset(lambda : post_data["post_thumbnail"])):
            #// Empty value deletes, non-empty value adds/updates.
            if (not post_data["post_thumbnail"]):
                delete_post_thumbnail(post_ID)
            elif (not get_post(absint(post_data["post_thumbnail"]))):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
            # end if
            set_post_thumbnail(post_ID, post_data["post_thumbnail"])
            content_struct["post_thumbnail"] = None
        # end if
        if (php_isset(lambda : post_data["custom_fields"])):
            self.set_custom_fields(post_ID, post_data["custom_fields"])
        # end if
        if (php_isset(lambda : post_data["terms"])) or (php_isset(lambda : post_data["terms_names"])):
            post_type_taxonomies = get_object_taxonomies(post_data["post_type"], "objects")
            #// Accumulate term IDs from terms and terms_names.
            terms = Array()
            #// First validate the terms specified by ID.
            if (php_isset(lambda : post_data["terms"])) and php_is_array(post_data["terms"]):
                taxonomies = php_array_keys(post_data["terms"])
                #// Validating term ids.
                for taxonomy in taxonomies:
                    if (not php_array_key_exists(taxonomy, post_type_taxonomies)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, one of the given taxonomies is not supported by the post type.")))
                    # end if
                    if (not current_user_can(post_type_taxonomies[taxonomy].cap.assign_terms)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign a term to one of the given taxonomies.")))
                    # end if
                    term_ids = post_data["terms"][taxonomy]
                    terms[taxonomy] = Array()
                    for term_id in term_ids:
                        term = get_term_by("id", term_id, taxonomy)
                        if (not term):
                            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid term ID.")))
                        # end if
                        terms[taxonomy][-1] = int(term_id)
                    # end for
                # end for
            # end if
            #// Now validate terms specified by name.
            if (php_isset(lambda : post_data["terms_names"])) and php_is_array(post_data["terms_names"]):
                taxonomies = php_array_keys(post_data["terms_names"])
                for taxonomy in taxonomies:
                    if (not php_array_key_exists(taxonomy, post_type_taxonomies)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, one of the given taxonomies is not supported by the post type.")))
                    # end if
                    if (not current_user_can(post_type_taxonomies[taxonomy].cap.assign_terms)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign a term to one of the given taxonomies.")))
                    # end if
                    #// 
                    #// For hierarchical taxonomies, we can't assign a term when multiple terms
                    #// in the hierarchy share the same name.
                    #//
                    ambiguous_terms = Array()
                    if is_taxonomy_hierarchical(taxonomy):
                        tax_term_names = get_terms(Array({"taxonomy": taxonomy, "fields": "names", "hide_empty": False}))
                        #// Count the number of terms with the same name.
                        tax_term_names_count = php_array_count_values(tax_term_names)
                        #// Filter out non-ambiguous term names.
                        ambiguous_tax_term_counts = php_array_filter(tax_term_names_count, Array(self, "_is_greater_than_one"))
                        ambiguous_terms = php_array_keys(ambiguous_tax_term_counts)
                    # end if
                    term_names = post_data["terms_names"][taxonomy]
                    for term_name in term_names:
                        if php_in_array(term_name, ambiguous_terms):
                            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Ambiguous term name used in a hierarchical taxonomy. Please use term ID instead.")))
                        # end if
                        term = get_term_by("name", term_name, taxonomy)
                        if (not term):
                            #// Term doesn't exist, so check that the user is allowed to create new terms.
                            if (not current_user_can(post_type_taxonomies[taxonomy].cap.edit_terms)):
                                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to add a term to one of the given taxonomies.")))
                            # end if
                            #// Create the new term.
                            term_info = wp_insert_term(term_name, taxonomy)
                            if is_wp_error(term_info):
                                return php_new_class("IXR_Error", lambda : IXR_Error(500, term_info.get_error_message()))
                            # end if
                            terms[taxonomy][-1] = int(term_info["term_id"])
                        else:
                            terms[taxonomy][-1] = int(term.term_id)
                        # end if
                    # end for
                # end for
            # end if
            post_data["tax_input"] = terms
            post_data["terms"] = None
            post_data["terms_names"] = None
        # end if
        if (php_isset(lambda : post_data["post_format"])):
            format = set_post_format(post_ID, post_data["post_format"])
            if is_wp_error(format):
                return php_new_class("IXR_Error", lambda : IXR_Error(500, format.get_error_message()))
            # end if
            post_data["post_format"] = None
        # end if
        #// Handle enclosures.
        enclosure = post_data["enclosure"] if (php_isset(lambda : post_data["enclosure"])) else None
        self.add_enclosure_if_new(post_ID, enclosure)
        self.attach_uploads(post_ID, post_data["post_content"])
        #// 
        #// Filters post data array to be inserted via XML-RPC.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array $post_data      Parsed array of post data.
        #// @param array $content_struct Post data array.
        #//
        post_data = apply_filters("xmlrpc_wp_insert_post_data", post_data, content_struct)
        post_ID = wp_update_post(post_data, True) if update else wp_insert_post(post_data, True)
        if is_wp_error(post_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, post_ID.get_error_message()))
        # end if
        if (not post_ID):
            if update:
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, the post could not be updated.")))
            else:
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, the post could not be created.")))
            # end if
        # end if
        return php_strval(post_ID)
    # end def _insert_post
    #// 
    #// Edit a post for any registered post type.
    #// 
    #// The $content_struct parameter only needs to contain fields that
    #// should be changed. All other fields will retain their existing values.
    #// 
    #// @since 3.4.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id        Blog ID (unused).
    #// @type string $username       Username.
    #// @type string $password       Password.
    #// @type int    $post_id        Post ID.
    #// @type array  $content_struct Extra content arguments.
    #// }
    #// @return true|IXR_Error True on success, IXR_Error on failure.
    #//
    def wp_editpost(self, args=None):
        
        if (not self.minimum_args(args, 5)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        post_id = int(args[3])
        content_struct = args[4]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editPost")
        post = get_post(post_id, ARRAY_A)
        if php_empty(lambda : post["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (php_isset(lambda : content_struct["if_not_modified_since"])):
            #// If the post has been modified since the date provided, return an error.
            if mysql2date("U", post["post_modified_gmt"]) > content_struct["if_not_modified_since"].gettimestamp():
                return php_new_class("IXR_Error", lambda : IXR_Error(409, __("There is a revision of this post that is more recent.")))
            # end if
        # end if
        #// Convert the date field back to IXR form.
        post["post_date"] = self._convert_date(post["post_date"])
        #// 
        #// Ignore the existing GMT date if it is empty or a non-GMT date was supplied in $content_struct,
        #// since _insert_post() will ignore the non-GMT date if the GMT date is set.
        #//
        if "0000-00-00 00:00:00" == post["post_date_gmt"] or (php_isset(lambda : content_struct["post_date"])):
            post["post_date_gmt"] = None
        else:
            post["post_date_gmt"] = self._convert_date(post["post_date_gmt"])
        # end if
        #// 
        #// If the API client did not provide 'post_date', then we must not perpetuate the value that
        #// was stored in the database, or it will appear to be an intentional edit. Conveying it here
        #// as if it was coming from the API client will cause an otherwise zeroed out 'post_date_gmt'
        #// to get set with the value that was originally stored in the database when the draft was created.
        #//
        if (not (php_isset(lambda : content_struct["post_date"]))):
            post["post_date"] = None
        # end if
        self.escape(post)
        merged_content_struct = php_array_merge(post, content_struct)
        retval = self._insert_post(user, merged_content_struct)
        if type(retval).__name__ == "IXR_Error":
            return retval
        # end if
        return True
    # end def wp_editpost
    #// 
    #// Delete a post for any registered post type.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_delete_post()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type int    $post_id  Post ID.
    #// }
    #// @return true|IXR_Error True on success, IXR_Error instance on failure.
    #//
    def wp_deletepost(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        post_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deletePost")
        post = get_post(post_id, ARRAY_A)
        if php_empty(lambda : post["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("delete_post", post_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this post.")))
        # end if
        result = wp_delete_post(post_id)
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be deleted.")))
        # end if
        return True
    # end def wp_deletepost
    #// 
    #// Retrieve a post.
    #// 
    #// @since 3.4.0
    #// 
    #// The optional $fields parameter specifies what fields will be included
    #// in the response array. This should be a list of field names. 'post_id' will
    #// always be included in the response regardless of the value of $fields.
    #// 
    #// Instead of, or in addition to, individual field names, conceptual group
    #// names can be used to specify multiple fields. The available conceptual
    #// groups are 'post' (all basic fields), 'taxonomies', 'custom_fields',
    #// and 'enclosure'.
    #// 
    #// @see get_post()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type int    $post_id  Post ID.
    #// @type array  $fields   The subset of post type fields to return.
    #// }
    #// @return array|IXR_Error Array contains (based on $fields parameter):
    #// - 'post_id'
    #// - 'post_title'
    #// - 'post_date'
    #// - 'post_date_gmt'
    #// - 'post_modified'
    #// - 'post_modified_gmt'
    #// - 'post_status'
    #// - 'post_type'
    #// - 'post_name'
    #// - 'post_author'
    #// - 'post_password'
    #// - 'post_excerpt'
    #// - 'post_content'
    #// - 'link'
    #// - 'comment_status'
    #// - 'ping_status'
    #// - 'sticky'
    #// - 'custom_fields'
    #// - 'terms'
    #// - 'categories'
    #// - 'tags'
    #// - 'enclosure'
    #//
    def wp_getpost(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        post_id = int(args[3])
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// 
            #// Filters the list of post query fields used by the given XML-RPC method.
            #// 
            #// @since 3.4.0
            #// 
            #// @param array  $fields Array of post fields. Default array contains 'post', 'terms', and 'custom_fields'.
            #// @param string $method Method name.
            #//
            fields = apply_filters("xmlrpc_default_post_fields", Array("post", "terms", "custom_fields"), "wp.getPost")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPost")
        post = get_post(post_id, ARRAY_A)
        if php_empty(lambda : post["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        return self._prepare_post(post, fields)
    # end def wp_getpost
    #// 
    #// Retrieve posts.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_get_recent_posts()
    #// @see wp_getPost() for more on `$fields`
    #// @see get_posts() for more on `$filter` values
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type array  $filter   Optional. Modifies the query used to retrieve posts. Accepts 'post_type',
    #// 'post_status', 'number', 'offset', 'orderby', 's', and 'order'.
    #// Default empty array.
    #// @type array  $fields   Optional. The subset of post type fields to return in the response array.
    #// }
    #// @return array|IXR_Error Array contains a collection of posts.
    #//
    def wp_getposts(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        filter = args[3] if (php_isset(lambda : args[3])) else Array()
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields = apply_filters("xmlrpc_default_post_fields", Array("post", "terms", "custom_fields"), "wp.getPosts")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPosts")
        query = Array()
        if (php_isset(lambda : filter["post_type"])):
            post_type = get_post_type_object(filter["post_type"])
            if (not bool(post_type)):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid post type.")))
            # end if
        else:
            post_type = get_post_type_object("post")
        # end if
        if (not current_user_can(post_type.cap.edit_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts in this post type.")))
        # end if
        query["post_type"] = post_type.name
        if (php_isset(lambda : filter["post_status"])):
            query["post_status"] = filter["post_status"]
        # end if
        if (php_isset(lambda : filter["number"])):
            query["numberposts"] = absint(filter["number"])
        # end if
        if (php_isset(lambda : filter["offset"])):
            query["offset"] = absint(filter["offset"])
        # end if
        if (php_isset(lambda : filter["orderby"])):
            query["orderby"] = filter["orderby"]
            if (php_isset(lambda : filter["order"])):
                query["order"] = filter["order"]
            # end if
        # end if
        if (php_isset(lambda : filter["s"])):
            query["s"] = filter["s"]
        # end if
        posts_list = wp_get_recent_posts(query)
        if (not posts_list):
            return Array()
        # end if
        #// Holds all the posts data.
        struct = Array()
        for post in posts_list:
            if (not current_user_can("edit_post", post["ID"])):
                continue
            # end if
            struct[-1] = self._prepare_post(post, fields)
        # end for
        return struct
    # end def wp_getposts
    #// 
    #// Create a new term.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_insert_term()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id        Blog ID (unused).
    #// @type string $username       Username.
    #// @type string $password       Password.
    #// @type array  $content_struct Content struct for adding a new term. The struct must contain
    #// the term 'name' and 'taxonomy'. Optional accepted values include
    #// 'parent', 'description', and 'slug'.
    #// }
    #// @return int|IXR_Error The term ID on success, or an IXR_Error object on failure.
    #//
    def wp_newterm(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        content_struct = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newTerm")
        if (not taxonomy_exists(content_struct["taxonomy"])):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy = get_taxonomy(content_struct["taxonomy"])
        if (not current_user_can(taxonomy.cap.edit_terms)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create terms in this taxonomy.")))
        # end if
        taxonomy = taxonomy
        #// Hold the data of the term.
        term_data = Array()
        term_data["name"] = php_trim(content_struct["name"])
        if php_empty(lambda : term_data["name"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("The term name cannot be empty.")))
        # end if
        if (php_isset(lambda : content_struct["parent"])):
            if (not taxonomy["hierarchical"]):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("This taxonomy is not hierarchical.")))
            # end if
            parent_term_id = int(content_struct["parent"])
            parent_term = get_term(parent_term_id, taxonomy["name"])
            if is_wp_error(parent_term):
                return php_new_class("IXR_Error", lambda : IXR_Error(500, parent_term.get_error_message()))
            # end if
            if (not parent_term):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Parent term does not exist.")))
            # end if
            term_data["parent"] = content_struct["parent"]
        # end if
        if (php_isset(lambda : content_struct["description"])):
            term_data["description"] = content_struct["description"]
        # end if
        if (php_isset(lambda : content_struct["slug"])):
            term_data["slug"] = content_struct["slug"]
        # end if
        term = wp_insert_term(term_data["name"], taxonomy["name"], term_data)
        if is_wp_error(term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term.get_error_message()))
        # end if
        if (not term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the term could not be created.")))
        # end if
        #// Add term meta.
        if (php_isset(lambda : content_struct["custom_fields"])):
            self.set_term_custom_fields(term["term_id"], content_struct["custom_fields"])
        # end if
        return php_strval(term["term_id"])
    # end def wp_newterm
    #// 
    #// Edit a term.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_update_term()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id        Blog ID (unused).
    #// @type string $username       Username.
    #// @type string $password       Password.
    #// @type int    $term_id        Term ID.
    #// @type array  $content_struct Content struct for editing a term. The struct must contain the
    #// term ''taxonomy'. Optional accepted values include 'name', 'parent',
    #// 'description', and 'slug'.
    #// }
    #// @return true|IXR_Error True on success, IXR_Error instance on failure.
    #//
    def wp_editterm(self, args=None):
        
        if (not self.minimum_args(args, 5)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        term_id = int(args[3])
        content_struct = args[4]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editTerm")
        if (not taxonomy_exists(content_struct["taxonomy"])):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy = get_taxonomy(content_struct["taxonomy"])
        taxonomy = taxonomy
        #// Hold the data of the term.
        term_data = Array()
        term = get_term(term_id, content_struct["taxonomy"])
        if is_wp_error(term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term.get_error_message()))
        # end if
        if (not term):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid term ID.")))
        # end if
        if (not current_user_can("edit_term", term_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this term.")))
        # end if
        if (php_isset(lambda : content_struct["name"])):
            term_data["name"] = php_trim(content_struct["name"])
            if php_empty(lambda : term_data["name"]):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("The term name cannot be empty.")))
            # end if
        # end if
        if (not php_empty(lambda : content_struct["parent"])):
            if (not taxonomy["hierarchical"]):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Cannot set parent term, taxonomy is not hierarchical.")))
            # end if
            parent_term_id = int(content_struct["parent"])
            parent_term = get_term(parent_term_id, taxonomy["name"])
            if is_wp_error(parent_term):
                return php_new_class("IXR_Error", lambda : IXR_Error(500, parent_term.get_error_message()))
            # end if
            if (not parent_term):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Parent term does not exist.")))
            # end if
            term_data["parent"] = content_struct["parent"]
        # end if
        if (php_isset(lambda : content_struct["description"])):
            term_data["description"] = content_struct["description"]
        # end if
        if (php_isset(lambda : content_struct["slug"])):
            term_data["slug"] = content_struct["slug"]
        # end if
        term = wp_update_term(term_id, taxonomy["name"], term_data)
        if is_wp_error(term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term.get_error_message()))
        # end if
        if (not term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, editing the term failed.")))
        # end if
        #// Update term meta.
        if (php_isset(lambda : content_struct["custom_fields"])):
            self.set_term_custom_fields(term_id, content_struct["custom_fields"])
        # end if
        return True
    # end def wp_editterm
    #// 
    #// Delete a term.
    #// 
    #// @since 3.4.0
    #// 
    #// @see wp_delete_term()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id      Blog ID (unused).
    #// @type string $username     Username.
    #// @type string $password     Password.
    #// @type string $taxnomy_name Taxonomy name.
    #// @type int    $term_id      Term ID.
    #// }
    #// @return bool|IXR_Error True on success, IXR_Error instance on failure.
    #//
    def wp_deleteterm(self, args=None):
        
        if (not self.minimum_args(args, 5)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        taxonomy = args[3]
        term_id = int(args[4])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deleteTerm")
        if (not taxonomy_exists(taxonomy)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy = get_taxonomy(taxonomy)
        term = get_term(term_id, taxonomy.name)
        if is_wp_error(term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term.get_error_message()))
        # end if
        if (not term):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid term ID.")))
        # end if
        if (not current_user_can("delete_term", term_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this term.")))
        # end if
        result = wp_delete_term(term_id, taxonomy.name)
        if is_wp_error(result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term.get_error_message()))
        # end if
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, deleting the term failed.")))
        # end if
        return result
    # end def wp_deleteterm
    #// 
    #// Retrieve a term.
    #// 
    #// @since 3.4.0
    #// 
    #// @see get_term()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type string $taxnomy  Taxonomy name.
    #// @type string $term_id  Term ID.
    #// }
    #// @return array|IXR_Error IXR_Error on failure, array on success, containing:
    #// - 'term_id'
    #// - 'name'
    #// - 'slug'
    #// - 'term_group'
    #// - 'term_taxonomy_id'
    #// - 'taxonomy'
    #// - 'description'
    #// - 'parent'
    #// - 'count'
    #//
    def wp_getterm(self, args=None):
        
        if (not self.minimum_args(args, 5)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        taxonomy = args[3]
        term_id = int(args[4])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTerm")
        if (not taxonomy_exists(taxonomy)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy = get_taxonomy(taxonomy)
        term = get_term(term_id, taxonomy.name, ARRAY_A)
        if is_wp_error(term):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term.get_error_message()))
        # end if
        if (not term):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid term ID.")))
        # end if
        if (not current_user_can("assign_term", term_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign this term.")))
        # end if
        return self._prepare_term(term)
    # end def wp_getterm
    #// 
    #// Retrieve all terms for a taxonomy.
    #// 
    #// @since 3.4.0
    #// 
    #// The optional $filter parameter modifies the query used to retrieve terms.
    #// Accepted keys are 'number', 'offset', 'orderby', 'order', 'hide_empty', and 'search'.
    #// 
    #// @see get_terms()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type string $taxnomy  Taxonomy name.
    #// @type array  $filter   Optional. Modifies the query used to retrieve posts. Accepts 'number',
    #// 'offset', 'orderby', 'order', 'hide_empty', and 'search'. Default empty array.
    #// }
    #// @return array|IXR_Error An associative array of terms data on success, IXR_Error instance otherwise.
    #//
    def wp_getterms(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        taxonomy = args[3]
        filter = args[4] if (php_isset(lambda : args[4])) else Array()
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTerms")
        if (not taxonomy_exists(taxonomy)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy = get_taxonomy(taxonomy)
        if (not current_user_can(taxonomy.cap.assign_terms)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign terms in this taxonomy.")))
        # end if
        query = Array({"taxonomy": taxonomy.name})
        if (php_isset(lambda : filter["number"])):
            query["number"] = absint(filter["number"])
        # end if
        if (php_isset(lambda : filter["offset"])):
            query["offset"] = absint(filter["offset"])
        # end if
        if (php_isset(lambda : filter["orderby"])):
            query["orderby"] = filter["orderby"]
            if (php_isset(lambda : filter["order"])):
                query["order"] = filter["order"]
            # end if
        # end if
        if (php_isset(lambda : filter["hide_empty"])):
            query["hide_empty"] = filter["hide_empty"]
        else:
            query["get"] = "all"
        # end if
        if (php_isset(lambda : filter["search"])):
            query["search"] = filter["search"]
        # end if
        terms = get_terms(query)
        if is_wp_error(terms):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, terms.get_error_message()))
        # end if
        struct = Array()
        for term in terms:
            struct[-1] = self._prepare_term(term)
        # end for
        return struct
    # end def wp_getterms
    #// 
    #// Retrieve a taxonomy.
    #// 
    #// @since 3.4.0
    #// 
    #// @see get_taxonomy()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type string $taxnomy  Taxonomy name.
    #// @type array  $fields   Optional. Array of taxonomy fields to limit to in the return.
    #// Accepts 'labels', 'cap', 'menu', and 'object_type'.
    #// Default empty array.
    #// }
    #// @return array|IXR_Error An array of taxonomy data on success, IXR_Error instance otherwise.
    #//
    def wp_gettaxonomy(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        taxonomy = args[3]
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// 
            #// Filters the taxonomy query fields used by the given XML-RPC method.
            #// 
            #// @since 3.4.0
            #// 
            #// @param array  $fields An array of taxonomy fields to retrieve.
            #// @param string $method The method name.
            #//
            fields = apply_filters("xmlrpc_default_taxonomy_fields", Array("labels", "cap", "object_type"), "wp.getTaxonomy")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTaxonomy")
        if (not taxonomy_exists(taxonomy)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy = get_taxonomy(taxonomy)
        if (not current_user_can(taxonomy.cap.assign_terms)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign terms in this taxonomy.")))
        # end if
        return self._prepare_taxonomy(taxonomy, fields)
    # end def wp_gettaxonomy
    #// 
    #// Retrieve all taxonomies.
    #// 
    #// @since 3.4.0
    #// 
    #// @see get_taxonomies()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id  Blog ID (unused).
    #// @type string $username Username.
    #// @type string $password Password.
    #// @type array  $filter   Optional. An array of arguments for retrieving taxonomies.
    #// @type array  $fields   Optional. The subset of taxonomy fields to return.
    #// }
    #// @return array|IXR_Error An associative array of taxonomy data with returned fields determined
    #// by `$fields`, or an IXR_Error instance on failure.
    #//
    def wp_gettaxonomies(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        filter = args[3] if (php_isset(lambda : args[3])) else Array({"public": True})
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields = apply_filters("xmlrpc_default_taxonomy_fields", Array("labels", "cap", "object_type"), "wp.getTaxonomies")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTaxonomies")
        taxonomies = get_taxonomies(filter, "objects")
        #// Holds all the taxonomy data.
        struct = Array()
        for taxonomy in taxonomies:
            #// Capability check for post types.
            if (not current_user_can(taxonomy.cap.assign_terms)):
                continue
            # end if
            struct[-1] = self._prepare_taxonomy(taxonomy, fields)
        # end for
        return struct
    # end def wp_gettaxonomies
    #// 
    #// Retrieve a user.
    #// 
    #// The optional $fields parameter specifies what fields will be included
    #// in the response array. This should be a list of field names. 'user_id' will
    #// always be included in the response regardless of the value of $fields.
    #// 
    #// Instead of, or in addition to, individual field names, conceptual group
    #// names can be used to specify multiple fields. The available conceptual
    #// groups are 'basic' and 'all'.
    #// 
    #// @uses get_userdata()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $user_id
    #// @type array  $fields (optional)
    #// }
    #// @return array|IXR_Error Array contains (based on $fields parameter):
    #// - 'user_id'
    #// - 'username'
    #// - 'first_name'
    #// - 'last_name'
    #// - 'registered'
    #// - 'bio'
    #// - 'email'
    #// - 'nickname'
    #// - 'nicename'
    #// - 'url'
    #// - 'display_name'
    #// - 'roles'
    #//
    def wp_getuser(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        user_id = int(args[3])
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// 
            #// Filters the default user query fields used by the given XML-RPC method.
            #// 
            #// @since 3.5.0
            #// 
            #// @param array  $fields User query fields for given method. Default 'all'.
            #// @param string $method The method name.
            #//
            fields = apply_filters("xmlrpc_default_user_fields", Array("all"), "wp.getUser")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getUser")
        if (not current_user_can("edit_user", user_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this user.")))
        # end if
        user_data = get_userdata(user_id)
        if (not user_data):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid user ID.")))
        # end if
        return self._prepare_user(user_data, fields)
    # end def wp_getuser
    #// 
    #// Retrieve users.
    #// 
    #// The optional $filter parameter modifies the query used to retrieve users.
    #// Accepted keys are 'number' (default: 50), 'offset' (default: 0), 'role',
    #// 'who', 'orderby', and 'order'.
    #// 
    #// The optional $fields parameter specifies what fields will be included
    #// in the response array.
    #// 
    #// @uses get_users()
    #// @see wp_getUser() for more on $fields and return values
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $filter (optional)
    #// @type array  $fields (optional)
    #// }
    #// @return array|IXR_Error users data
    #//
    def wp_getusers(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        filter = args[3] if (php_isset(lambda : args[3])) else Array()
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields = apply_filters("xmlrpc_default_user_fields", Array("all"), "wp.getUsers")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getUsers")
        if (not current_user_can("list_users")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to list users.")))
        # end if
        query = Array({"fields": "all_with_meta"})
        query["number"] = absint(filter["number"]) if (php_isset(lambda : filter["number"])) else 50
        query["offset"] = absint(filter["offset"]) if (php_isset(lambda : filter["offset"])) else 0
        if (php_isset(lambda : filter["orderby"])):
            query["orderby"] = filter["orderby"]
            if (php_isset(lambda : filter["order"])):
                query["order"] = filter["order"]
            # end if
        # end if
        if (php_isset(lambda : filter["role"])):
            if get_role(filter["role"]) == None:
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid role.")))
            # end if
            query["role"] = filter["role"]
        # end if
        if (php_isset(lambda : filter["who"])):
            query["who"] = filter["who"]
        # end if
        users = get_users(query)
        _users = Array()
        for user_data in users:
            if current_user_can("edit_user", user_data.ID):
                _users[-1] = self._prepare_user(user_data, fields)
            # end if
        # end for
        return _users
    # end def wp_getusers
    #// 
    #// Retrieve information about the requesting user.
    #// 
    #// @uses get_userdata()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $fields (optional)
    #// }
    #// @return array|IXR_Error (@see wp_getUser)
    #//
    def wp_getprofile(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        if (php_isset(lambda : args[3])):
            fields = args[3]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields = apply_filters("xmlrpc_default_user_fields", Array("all"), "wp.getProfile")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getProfile")
        if (not current_user_can("edit_user", user.ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit your profile.")))
        # end if
        user_data = get_userdata(user.ID)
        return self._prepare_user(user_data, fields)
    # end def wp_getprofile
    #// 
    #// Edit user's profile.
    #// 
    #// @uses wp_update_user()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $content_struct It can optionally contain:
    #// - 'first_name'
    #// - 'last_name'
    #// - 'website'
    #// - 'display_name'
    #// - 'nickname'
    #// - 'nicename'
    #// - 'bio'
    #// }
    #// @return true|IXR_Error True, on success.
    #//
    def wp_editprofile(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        content_struct = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editProfile")
        if (not current_user_can("edit_user", user.ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit your profile.")))
        # end if
        #// Holds data of the user.
        user_data = Array()
        user_data["ID"] = user.ID
        #// Only set the user details if they were given.
        if (php_isset(lambda : content_struct["first_name"])):
            user_data["first_name"] = content_struct["first_name"]
        # end if
        if (php_isset(lambda : content_struct["last_name"])):
            user_data["last_name"] = content_struct["last_name"]
        # end if
        if (php_isset(lambda : content_struct["url"])):
            user_data["user_url"] = content_struct["url"]
        # end if
        if (php_isset(lambda : content_struct["display_name"])):
            user_data["display_name"] = content_struct["display_name"]
        # end if
        if (php_isset(lambda : content_struct["nickname"])):
            user_data["nickname"] = content_struct["nickname"]
        # end if
        if (php_isset(lambda : content_struct["nicename"])):
            user_data["user_nicename"] = content_struct["nicename"]
        # end if
        if (php_isset(lambda : content_struct["bio"])):
            user_data["description"] = content_struct["bio"]
        # end if
        result = wp_update_user(user_data)
        if is_wp_error(result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, result.get_error_message()))
        # end if
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the user could not be updated.")))
        # end if
        return True
    # end def wp_editprofile
    #// 
    #// Retrieve page.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type int    $page_id
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getpage(self, args=None):
        
        self.escape(args)
        page_id = int(args[1])
        username = args[2]
        password = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        page = get_post(page_id)
        if (not page):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_page", page_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this page.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPage")
        #// If we found the page then format the data.
        if page.ID and "page" == page.post_type:
            return self._prepare_page(page)
        else:
            #// If the page doesn't exist, indicate that.
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such page.")))
        # end if
    # end def wp_getpage
    #// 
    #// Retrieve Pages.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $num_pages
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getpages(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        num_pages = int(args[3]) if (php_isset(lambda : args[3])) else 10
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit pages.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPages")
        pages = get_posts(Array({"post_type": "page", "post_status": "any", "numberposts": num_pages}))
        num_pages = php_count(pages)
        #// If we have pages, put together their info.
        if num_pages >= 1:
            pages_struct = Array()
            for page in pages:
                if current_user_can("edit_page", page.ID):
                    pages_struct[-1] = self._prepare_page(page)
                # end if
            # end for
            return pages_struct
        # end if
        return Array()
    # end def wp_getpages
    #// 
    #// Create new page.
    #// 
    #// @since 2.2.0
    #// 
    #// @see wp_xmlrpc_server::mw_newPost()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $content_struct
    #// }
    #// @return int|IXR_Error
    #//
    def wp_newpage(self, args=None):
        
        #// Items not escaped here will be escaped in wp_newPost().
        username = self.escape(args[1])
        password = self.escape(args[2])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newPage")
        #// Mark this as content for a page.
        args[3]["post_type"] = "page"
        #// Let mw_newPost() do all of the heavy lifting.
        return self.mw_newpost(args)
    # end def wp_newpage
    #// 
    #// Delete page.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $page_id
    #// }
    #// @return true|IXR_Error True, if success.
    #//
    def wp_deletepage(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        page_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deletePage")
        #// Get the current page based on the 'page_id' and
        #// make sure it is a page and not a post.
        actual_page = get_post(page_id, ARRAY_A)
        if (not actual_page) or "page" != actual_page["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such page.")))
        # end if
        #// Make sure the user can delete pages.
        if (not current_user_can("delete_page", page_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this page.")))
        # end if
        #// Attempt to delete the page.
        result = wp_delete_post(page_id)
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Failed to delete the page.")))
        # end if
        #// 
        #// Fires after a page has been successfully deleted via XML-RPC.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $page_id ID of the deleted page.
        #// @param array $args    An array of arguments to delete the page.
        #//
        do_action("xmlrpc_call_success_wp_deletePage", page_id, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return True
    # end def wp_deletepage
    #// 
    #// Edit page.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type int    $page_id
    #// @type string $username
    #// @type string $password
    #// @type string $content
    #// @type string $publish
    #// }
    #// @return array|IXR_Error
    #//
    def wp_editpage(self, args=None):
        
        #// Items will be escaped in mw_editPost().
        page_id = int(args[1])
        username = args[2]
        password = args[3]
        content = args[4]
        publish = args[5]
        escaped_username = self.escape(username)
        escaped_password = self.escape(password)
        user = self.login(escaped_username, escaped_password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editPage")
        #// Get the page data and make sure it is a page.
        actual_page = get_post(page_id, ARRAY_A)
        if (not actual_page) or "page" != actual_page["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such page.")))
        # end if
        #// Make sure the user is allowed to edit pages.
        if (not current_user_can("edit_page", page_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this page.")))
        # end if
        #// Mark this as content for a page.
        content["post_type"] = "page"
        #// Arrange args in the way mw_editPost() understands.
        args = Array(page_id, username, password, content, publish)
        #// Let mw_editPost() do all of the heavy lifting.
        return self.mw_editpost(args)
    # end def wp_editpage
    #// 
    #// Retrieve page list.
    #// 
    #// @since 2.2.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getpagelist(self, args=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit pages.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPageList")
        #// Get list of page IDs and titles.
        page_list = wpdb.get_results(str("""\n          SELECT ID page_id,\n                post_title page_title,\n                post_parent page_parent_id,\n               post_date_gmt,\n                post_date,\n                post_status\n           FROM """) + str(wpdb.posts) + str("""\n         WHERE post_type = 'page'\n          ORDER BY ID\n       """))
        #// The date needs to be formatted properly.
        num_pages = php_count(page_list)
        i = 0
        while i < num_pages:
            
            page_list[i].dateCreated = self._convert_date(page_list[i].post_date)
            page_list[i].date_created_gmt = self._convert_date_gmt(page_list[i].post_date_gmt, page_list[i].post_date)
            page_list[i].post_date_gmt = None
            page_list[i].post_date = None
            page_list[i].post_status = None
            i += 1
        # end while
        return page_list
    # end def wp_getpagelist
    #// 
    #// Retrieve authors list.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getauthors(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getAuthors")
        authors = Array()
        for user in get_users(Array({"fields": Array("ID", "user_login", "display_name")})):
            authors[-1] = Array({"user_id": user.ID, "user_login": user.user_login, "display_name": user.display_name})
        # end for
        return authors
    # end def wp_getauthors
    #// 
    #// Get list of all tags
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_gettags(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view tags.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getKeywords")
        tags = Array()
        all_tags = get_tags()
        if all_tags:
            for tag in all_tags:
                struct = Array()
                struct["tag_id"] = tag.term_id
                struct["name"] = tag.name
                struct["count"] = tag.count
                struct["slug"] = tag.slug
                struct["html_url"] = esc_html(get_tag_link(tag.term_id))
                struct["rss_url"] = esc_html(get_tag_feed_link(tag.term_id))
                tags[-1] = struct
            # end for
        # end if
        return tags
    # end def wp_gettags
    #// 
    #// Create new category.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $category
    #// }
    #// @return int|IXR_Error Category ID.
    #//
    def wp_newcategory(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        category = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newCategory")
        #// Make sure the user is allowed to add a category.
        if (not current_user_can("manage_categories")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to add a category.")))
        # end if
        #// If no slug was provided, make it empty
        #// so that WordPress will generate one.
        if php_empty(lambda : category["slug"]):
            category["slug"] = ""
        # end if
        #// If no parent_id was provided, make it empty
        #// so that it will be a top-level page (no parent).
        if (not (php_isset(lambda : category["parent_id"]))):
            category["parent_id"] = ""
        # end if
        #// If no description was provided, make it empty.
        if php_empty(lambda : category["description"]):
            category["description"] = ""
        # end if
        new_category = Array({"cat_name": category["name"], "category_nicename": category["slug"], "category_parent": category["parent_id"], "category_description": category["description"]})
        cat_id = wp_insert_category(new_category, True)
        if is_wp_error(cat_id):
            if "term_exists" == cat_id.get_error_code():
                return int(cat_id.get_error_data())
            else:
                return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the category could not be created.")))
            # end if
        elif (not cat_id):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the category could not be created.")))
        # end if
        #// 
        #// Fires after a new category has been successfully created via XML-RPC.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $cat_id ID of the new category.
        #// @param array $args   An array of new category arguments.
        #//
        do_action("xmlrpc_call_success_wp_newCategory", cat_id, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return cat_id
    # end def wp_newcategory
    #// 
    #// Remove category.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $category_id
    #// }
    #// @return bool|IXR_Error See wp_delete_term() for return info.
    #//
    def wp_deletecategory(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        category_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deleteCategory")
        if (not current_user_can("delete_term", category_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this category.")))
        # end if
        status = wp_delete_term(category_id, "category")
        if True == status:
            #// 
            #// Fires after a category has been successfully deleted via XML-RPC.
            #// 
            #// @since 3.4.0
            #// 
            #// @param int   $category_id ID of the deleted category.
            #// @param array $args        An array of arguments to delete the category.
            #//
            do_action("xmlrpc_call_success_wp_deleteCategory", category_id, args)
            pass
        # end if
        return status
    # end def wp_deletecategory
    #// 
    #// Retrieve category list.
    #// 
    #// @since 2.2.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $category
    #// @type int    $max_results
    #// }
    #// @return array|IXR_Error
    #//
    def wp_suggestcategories(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        category = args[3]
        max_results = int(args[4])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view categories.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.suggestCategories")
        category_suggestions = Array()
        args = Array({"get": "all", "number": max_results, "name__like": category})
        for cat in get_categories(args):
            category_suggestions[-1] = Array({"category_id": cat.term_id, "category_name": cat.name})
        # end for
        return category_suggestions
    # end def wp_suggestcategories
    #// 
    #// Retrieve comment.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $comment_id
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getcomment(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        comment_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getComment")
        comment = get_comment(comment_id)
        if (not comment):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid comment ID.")))
        # end if
        if (not current_user_can("edit_comment", comment_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to moderate or edit this comment.")))
        # end if
        return self._prepare_comment(comment)
    # end def wp_getcomment
    #// 
    #// Retrieve comments.
    #// 
    #// Besides the common blog_id (unused), username, and password arguments, it takes a filter
    #// array as last argument.
    #// 
    #// Accepted 'filter' keys are 'status', 'post_id', 'offset', and 'number'.
    #// 
    #// The defaults are as follows:
    #// - 'status' - Default is ''. Filter by status (e.g., 'approve', 'hold')
    #// - 'post_id' - Default is ''. The post where the comment is posted. Empty string shows all comments.
    #// - 'number' - Default is 10. Total number of media items to retrieve.
    #// - 'offset' - Default is 0. See WP_Query::query() for more.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $struct
    #// }
    #// @return array|IXR_Error Contains a collection of comments. See wp_xmlrpc_server::wp_getComment() for a description of each item contents
    #//
    def wp_getcomments(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        struct = args[3] if (php_isset(lambda : args[3])) else Array()
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getComments")
        if (php_isset(lambda : struct["status"])):
            status = struct["status"]
        else:
            status = ""
        # end if
        if (not current_user_can("moderate_comments")) and "approve" != status:
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid comment status.")))
        # end if
        post_id = ""
        if (php_isset(lambda : struct["post_id"])):
            post_id = absint(struct["post_id"])
        # end if
        post_type = ""
        if (php_isset(lambda : struct["post_type"])):
            post_type_object = get_post_type_object(struct["post_type"])
            if (not post_type_object) or (not post_type_supports(post_type_object.name, "comments")):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post type.")))
            # end if
            post_type = struct["post_type"]
        # end if
        offset = 0
        if (php_isset(lambda : struct["offset"])):
            offset = absint(struct["offset"])
        # end if
        number = 10
        if (php_isset(lambda : struct["number"])):
            number = absint(struct["number"])
        # end if
        comments = get_comments(Array({"status": status, "post_id": post_id, "offset": offset, "number": number, "post_type": post_type}))
        comments_struct = Array()
        if php_is_array(comments):
            for comment in comments:
                comments_struct[-1] = self._prepare_comment(comment)
            # end for
        # end if
        return comments_struct
    # end def wp_getcomments
    #// 
    #// Delete a comment.
    #// 
    #// By default, the comment will be moved to the Trash instead of deleted.
    #// See wp_delete_comment() for more information on this behavior.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $comment_ID
    #// }
    #// @return bool|IXR_Error See wp_delete_comment().
    #//
    def wp_deletecomment(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        comment_ID = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not get_comment(comment_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid comment ID.")))
        # end if
        if (not current_user_can("edit_comment", comment_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to delete this comment.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deleteComment")
        status = wp_delete_comment(comment_ID)
        if status:
            #// 
            #// Fires after a comment has been successfully deleted via XML-RPC.
            #// 
            #// @since 3.4.0
            #// 
            #// @param int   $comment_ID ID of the deleted comment.
            #// @param array $args       An array of arguments to delete the comment.
            #//
            do_action("xmlrpc_call_success_wp_deleteComment", comment_ID, args)
            pass
        # end if
        return status
    # end def wp_deletecomment
    #// 
    #// Edit comment.
    #// 
    #// Besides the common blog_id (unused), username, and password arguments, it takes a
    #// comment_id integer and a content_struct array as last argument.
    #// 
    #// The allowed keys in the content_struct array are:
    #// - 'author'
    #// - 'author_url'
    #// - 'author_email'
    #// - 'content'
    #// - 'date_created_gmt'
    #// - 'status'. Common statuses are 'approve', 'hold', 'spam'. See get_comment_statuses() for more details
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $comment_ID
    #// @type array  $content_struct
    #// }
    #// @return true|IXR_Error True, on success.
    #//
    def wp_editcomment(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        comment_ID = int(args[3])
        content_struct = args[4]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not get_comment(comment_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid comment ID.")))
        # end if
        if (not current_user_can("edit_comment", comment_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to moderate or edit this comment.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editComment")
        comment = Array({"comment_ID": comment_ID})
        if (php_isset(lambda : content_struct["status"])):
            statuses = get_comment_statuses()
            statuses = php_array_keys(statuses)
            if (not php_in_array(content_struct["status"], statuses)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid comment status.")))
            # end if
            comment["comment_approved"] = content_struct["status"]
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : content_struct["date_created_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated = php_rtrim(content_struct["date_created_gmt"].getiso(), "Z") + "Z"
            comment["comment_date"] = get_date_from_gmt(dateCreated)
            comment["comment_date_gmt"] = iso8601_to_datetime(dateCreated, "gmt")
        # end if
        if (php_isset(lambda : content_struct["content"])):
            comment["comment_content"] = content_struct["content"]
        # end if
        if (php_isset(lambda : content_struct["author"])):
            comment["comment_author"] = content_struct["author"]
        # end if
        if (php_isset(lambda : content_struct["author_url"])):
            comment["comment_author_url"] = content_struct["author_url"]
        # end if
        if (php_isset(lambda : content_struct["author_email"])):
            comment["comment_author_email"] = content_struct["author_email"]
        # end if
        result = wp_update_comment(comment)
        if is_wp_error(result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, result.get_error_message()))
        # end if
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the comment could not be updated.")))
        # end if
        #// 
        #// Fires after a comment has been successfully updated via XML-RPC.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $comment_ID ID of the updated comment.
        #// @param array $args       An array of arguments to update the comment.
        #//
        do_action("xmlrpc_call_success_wp_editComment", comment_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return True
    # end def wp_editcomment
    #// 
    #// Create new comment.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int        $blog_id (unused)
    #// @type string     $username
    #// @type string     $password
    #// @type string|int $post
    #// @type array      $content_struct
    #// }
    #// @return int|IXR_Error See wp_new_comment().
    #//
    def wp_newcomment(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        post = args[3]
        content_struct = args[4]
        #// 
        #// Filters whether to allow anonymous comments over XML-RPC.
        #// 
        #// @since 2.7.0
        #// 
        #// @param bool $allow Whether to allow anonymous commenting via XML-RPC.
        #// Default false.
        #//
        allow_anon = apply_filters("xmlrpc_allow_anonymous_comments", False)
        user = self.login(username, password)
        if (not user):
            logged_in = False
            if allow_anon and get_option("comment_registration"):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you must be logged in to comment.")))
            elif (not allow_anon):
                return self.error
            # end if
        else:
            logged_in = True
        # end if
        if php_is_numeric(post):
            post_id = absint(post)
        else:
            post_id = url_to_postid(post)
        # end if
        if (not post_id):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not get_post(post_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not comments_open(post_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, comments are closed for this item.")))
        # end if
        if php_empty(lambda : content_struct["content"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Comment is required.")))
        # end if
        comment = Array({"comment_post_ID": post_id, "comment_content": content_struct["content"]})
        if logged_in:
            display_name = user.display_name
            user_email = user.user_email
            user_url = user.user_url
            comment["comment_author"] = self.escape(display_name)
            comment["comment_author_email"] = self.escape(user_email)
            comment["comment_author_url"] = self.escape(user_url)
            comment["user_ID"] = user.ID
        else:
            comment["comment_author"] = ""
            if (php_isset(lambda : content_struct["author"])):
                comment["comment_author"] = content_struct["author"]
            # end if
            comment["comment_author_email"] = ""
            if (php_isset(lambda : content_struct["author_email"])):
                comment["comment_author_email"] = content_struct["author_email"]
            # end if
            comment["comment_author_url"] = ""
            if (php_isset(lambda : content_struct["author_url"])):
                comment["comment_author_url"] = content_struct["author_url"]
            # end if
            comment["user_ID"] = 0
            if get_option("require_name_email"):
                if 6 > php_strlen(comment["comment_author_email"]) or "" == comment["comment_author"]:
                    return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Comment author name and email are required.")))
                elif (not is_email(comment["comment_author_email"])):
                    return php_new_class("IXR_Error", lambda : IXR_Error(403, __("A valid email address is required.")))
                # end if
            # end if
        # end if
        comment["comment_parent"] = absint(content_struct["comment_parent"]) if (php_isset(lambda : content_struct["comment_parent"])) else 0
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newComment")
        comment_ID = wp_new_comment(comment, True)
        if is_wp_error(comment_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, comment_ID.get_error_message()))
        # end if
        if (not comment_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Something went wrong.")))
        # end if
        #// 
        #// Fires after a new comment has been successfully created via XML-RPC.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $comment_ID ID of the new comment.
        #// @param array $args       An array of new comment arguments.
        #//
        do_action("xmlrpc_call_success_wp_newComment", comment_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return comment_ID
    # end def wp_newcomment
    #// 
    #// Retrieve all of the comment status.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getcommentstatuslist(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("publish_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getCommentStatusList")
        return get_comment_statuses()
    # end def wp_getcommentstatuslist
    #// 
    #// Retrieve comment count.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $post_id
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getcommentcount(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        post_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        post = get_post(post_id, ARRAY_A)
        if php_empty(lambda : post["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details of this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getCommentCount")
        count = wp_count_comments(post_id)
        return Array({"approved": count.approved, "awaiting_moderation": count.moderated, "spam": count.spam, "total_comments": count.total_comments})
    # end def wp_getcommentcount
    #// 
    #// Retrieve post statuses.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getpoststatuslist(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostStatusList")
        return get_post_statuses()
    # end def wp_getpoststatuslist
    #// 
    #// Retrieve page statuses.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getpagestatuslist(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPageStatusList")
        return get_page_statuses()
    # end def wp_getpagestatuslist
    #// 
    #// Retrieve page templates.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getpagetemplates(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        templates = get_page_templates()
        templates["Default"] = "default"
        return templates
    # end def wp_getpagetemplates
    #// 
    #// Retrieve blog options.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $options
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getoptions(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        options = args[3] if (php_isset(lambda : args[3])) else Array()
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// If no specific options where asked for, return all of them.
        if php_count(options) == 0:
            options = php_array_keys(self.blog_options)
        # end if
        return self._getoptions(options)
    # end def wp_getoptions
    #// 
    #// Retrieve blog options value from list.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $options Options to retrieve.
    #// @return array
    #//
    def _getoptions(self, options=None):
        
        data = Array()
        can_manage = current_user_can("manage_options")
        for option in options:
            if php_array_key_exists(option, self.blog_options):
                data[option] = self.blog_options[option]
                #// Is the value static or dynamic?
                if (php_isset(lambda : data[option]["option"])):
                    data[option]["value"] = get_option(data[option]["option"])
                    data[option]["option"] = None
                # end if
                if (not can_manage):
                    data[option]["readonly"] = True
                # end if
            # end if
        # end for
        return data
    # end def _getoptions
    #// 
    #// Update blog options.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $options
    #// }
    #// @return array|IXR_Error
    #//
    def wp_setoptions(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        options = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("manage_options")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to update options.")))
        # end if
        option_names = Array()
        for o_name,o_value in options:
            option_names[-1] = o_name
            if (not php_array_key_exists(o_name, self.blog_options)):
                continue
            # end if
            if True == self.blog_options[o_name]["readonly"]:
                continue
            # end if
            update_option(self.blog_options[o_name]["option"], wp_unslash(o_value))
        # end for
        #// Now return the updated values.
        return self._getoptions(option_names)
    # end def wp_setoptions
    #// 
    #// Retrieve a media item by ID
    #// 
    #// @since 3.1.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $attachment_id
    #// }
    #// @return array|IXR_Error Associative array contains:
    #// - 'date_created_gmt'
    #// - 'parent'
    #// - 'link'
    #// - 'thumbnail'
    #// - 'title'
    #// - 'caption'
    #// - 'description'
    #// - 'metadata'
    #//
    def wp_getmediaitem(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        attachment_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("upload_files")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to upload files.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getMediaItem")
        attachment = get_post(attachment_id)
        if (not attachment):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
        # end if
        return self._prepare_media_item(attachment)
    # end def wp_getmediaitem
    #// 
    #// Retrieves a collection of media library items (or attachments)
    #// 
    #// Besides the common blog_id (unused), username, and password arguments, it takes a filter
    #// array as last argument.
    #// 
    #// Accepted 'filter' keys are 'parent_id', 'mime_type', 'offset', and 'number'.
    #// 
    #// The defaults are as follows:
    #// - 'number' - Default is 5. Total number of media items to retrieve.
    #// - 'offset' - Default is 0. See WP_Query::query() for more.
    #// - 'parent_id' - Default is ''. The post where the media item is attached. Empty string shows all media items. 0 shows unattached media items.
    #// - 'mime_type' - Default is ''. Filter by mime type (e.g., 'image/jpeg', 'application/pdf')
    #// 
    #// @since 3.1.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $struct
    #// }
    #// @return array|IXR_Error Contains a collection of media items. See wp_xmlrpc_server::wp_getMediaItem() for a description of each item contents
    #//
    def wp_getmedialibrary(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        struct = args[3] if (php_isset(lambda : args[3])) else Array()
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("upload_files")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to upload files.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getMediaLibrary")
        parent_id = absint(struct["parent_id"]) if (php_isset(lambda : struct["parent_id"])) else ""
        mime_type = struct["mime_type"] if (php_isset(lambda : struct["mime_type"])) else ""
        offset = absint(struct["offset"]) if (php_isset(lambda : struct["offset"])) else 0
        number = absint(struct["number"]) if (php_isset(lambda : struct["number"])) else -1
        attachments = get_posts(Array({"post_type": "attachment", "post_parent": parent_id, "offset": offset, "numberposts": number, "post_mime_type": mime_type}))
        attachments_struct = Array()
        for attachment in attachments:
            attachments_struct[-1] = self._prepare_media_item(attachment)
        # end for
        return attachments_struct
    # end def wp_getmedialibrary
    #// 
    #// Retrieves a list of post formats used by the site.
    #// 
    #// @since 3.1.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error List of post formats, otherwise IXR_Error object.
    #//
    def wp_getpostformats(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostFormats")
        formats = get_post_format_strings()
        #// Find out if they want a list of currently supports formats.
        if (php_isset(lambda : args[3])) and php_is_array(args[3]):
            if args[3]["show-supported"]:
                if current_theme_supports("post-formats"):
                    supported = get_theme_support("post-formats")
                    data = Array()
                    data["all"] = formats
                    data["supported"] = supported[0]
                    formats = data
                # end if
            # end if
        # end if
        return formats
    # end def wp_getpostformats
    #// 
    #// Retrieves a post type
    #// 
    #// @since 3.4.0
    #// 
    #// @see get_post_type_object()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type string $post_type_name
    #// @type array  $fields (optional)
    #// }
    #// @return array|IXR_Error Array contains:
    #// - 'labels'
    #// - 'description'
    #// - 'capability_type'
    #// - 'cap'
    #// - 'map_meta_cap'
    #// - 'hierarchical'
    #// - 'menu_position'
    #// - 'taxonomies'
    #// - 'supports'
    #//
    def wp_getposttype(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        post_type_name = args[3]
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// 
            #// Filters the default query fields used by the given XML-RPC method.
            #// 
            #// @since 3.4.0
            #// 
            #// @param array  $fields An array of post type query fields for the given method.
            #// @param string $method The method name.
            #//
            fields = apply_filters("xmlrpc_default_posttype_fields", Array("labels", "cap", "taxonomies"), "wp.getPostType")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostType")
        if (not post_type_exists(post_type_name)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid post type.")))
        # end if
        post_type = get_post_type_object(post_type_name)
        if (not current_user_can(post_type.cap.edit_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts in this post type.")))
        # end if
        return self._prepare_post_type(post_type, fields)
    # end def wp_getposttype
    #// 
    #// Retrieves a post types
    #// 
    #// @since 3.4.0
    #// 
    #// @see get_post_types()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $filter (optional)
    #// @type array  $fields (optional)
    #// }
    #// @return array|IXR_Error
    #//
    def wp_getposttypes(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        filter = args[3] if (php_isset(lambda : args[3])) else Array({"public": True})
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields = apply_filters("xmlrpc_default_posttype_fields", Array("labels", "cap", "taxonomies"), "wp.getPostTypes")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostTypes")
        post_types = get_post_types(filter, "objects")
        struct = Array()
        for post_type in post_types:
            if (not current_user_can(post_type.cap.edit_posts)):
                continue
            # end if
            struct[post_type.name] = self._prepare_post_type(post_type, fields)
        # end for
        return struct
    # end def wp_getposttypes
    #// 
    #// Retrieve revisions for a specific post.
    #// 
    #// @since 3.5.0
    #// 
    #// The optional $fields parameter specifies what fields will be included
    #// in the response array.
    #// 
    #// @uses wp_get_post_revisions()
    #// @see wp_getPost() for more on $fields
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $post_id
    #// @type array  $fields (optional)
    #// }
    #// @return array|IXR_Error contains a collection of posts.
    #//
    def wp_getrevisions(self, args=None):
        
        if (not self.minimum_args(args, 4)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        post_id = int(args[3])
        if (php_isset(lambda : args[4])):
            fields = args[4]
        else:
            #// 
            #// Filters the default revision query fields used by the given XML-RPC method.
            #// 
            #// @since 3.5.0
            #// 
            #// @param array  $field  An array of revision query fields.
            #// @param string $method The method name.
            #//
            fields = apply_filters("xmlrpc_default_revision_fields", Array("post_date", "post_date_gmt"), "wp.getRevisions")
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getRevisions")
        post = get_post(post_id)
        if (not post):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_id)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// Check if revisions are enabled.
        if (not wp_revisions_enabled(post)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, revisions are disabled.")))
        # end if
        revisions = wp_get_post_revisions(post_id)
        if (not revisions):
            return Array()
        # end if
        struct = Array()
        for revision in revisions:
            if (not current_user_can("read_post", revision.ID)):
                continue
            # end if
            #// Skip autosaves.
            if wp_is_post_autosave(revision):
                continue
            # end if
            struct[-1] = self._prepare_post(get_object_vars(revision), fields)
        # end for
        return struct
    # end def wp_getrevisions
    #// 
    #// Restore a post revision
    #// 
    #// @since 3.5.0
    #// 
    #// @uses wp_restore_post_revision()
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $revision_id
    #// }
    #// @return bool|IXR_Error false if there was an error restoring, true if success.
    #//
    def wp_restorerevision(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        revision_id = int(args[3])
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.restoreRevision")
        revision = wp_get_post_revision(revision_id)
        if (not revision):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if wp_is_post_autosave(revision):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        post = get_post(revision.post_parent)
        if (not post):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", revision.post_parent)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// Check if revisions are disabled.
        if (not wp_revisions_enabled(post)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, revisions are disabled.")))
        # end if
        post = wp_restore_post_revision(revision_id)
        return bool(post)
    # end def wp_restorerevision
    #// 
    #// Blogger API functions.
    #// Specs on http://plant.blogger.com/api and https://groups.yahoo.com/group/bloggerDev
    #// 
    #// 
    #// Retrieve blogs that user owns.
    #// 
    #// Will make more sense once we support multiple blogs.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def blogger_getusersblogs(self, args=None):
        
        if (not self.minimum_args(args, 3)):
            return self.error
        # end if
        if is_multisite():
            return self._multisite_getusersblogs(args)
        # end if
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getUsersBlogs")
        is_admin = current_user_can("manage_options")
        struct = Array({"isAdmin": is_admin, "url": get_option("home") + "/", "blogid": "1", "blogName": get_option("blogname"), "xmlrpc": site_url("xmlrpc.php", "rpc")})
        return Array(struct)
    # end def blogger_getusersblogs
    #// 
    #// Private function for retrieving a users blogs for multisite setups
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type string $username Username.
    #// @type string $password Password.
    #// }
    #// @return array|IXR_Error
    #//
    def _multisite_getusersblogs(self, args=None):
        
        current_blog = get_site()
        domain = current_blog.domain
        path = current_blog.path + "xmlrpc.php"
        rpc = php_new_class("IXR_Client", lambda : IXR_Client(set_url_scheme(str("http://") + str(domain) + str(path))))
        rpc.query("wp.getUsersBlogs", args[1], args[2])
        blogs = rpc.getresponse()
        if (php_isset(lambda : blogs["faultCode"])):
            return php_new_class("IXR_Error", lambda : IXR_Error(blogs["faultCode"], blogs["faultString"]))
        # end if
        if PHP_SERVER["HTTP_HOST"] == domain and PHP_SERVER["REQUEST_URI"] == path:
            return blogs
        else:
            for blog in blogs:
                if php_strpos(blog["url"], PHP_SERVER["HTTP_HOST"]):
                    return Array(blog)
                # end if
            # end for
            return Array()
        # end if
    # end def _multisite_getusersblogs
    #// 
    #// Retrieve user's data.
    #// 
    #// Gives your client some info about you, so you don't have to.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def blogger_getuserinfo(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to access user data on this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getUserInfo")
        struct = Array({"nickname": user.nickname, "userid": user.ID, "url": user.user_url, "lastname": user.last_name, "firstname": user.first_name})
        return struct
    # end def blogger_getuserinfo
    #// 
    #// Retrieve post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def blogger_getpost(self, args=None):
        
        self.escape(args)
        post_ID = int(args[1])
        username = args[2]
        password = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        post_data = get_post(post_ID, ARRAY_A)
        if (not post_data):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getPost")
        categories = php_implode(",", wp_get_post_categories(post_ID))
        content = "<title>" + wp_unslash(post_data["post_title"]) + "</title>"
        content += "<category>" + categories + "</category>"
        content += wp_unslash(post_data["post_content"])
        struct = Array({"userid": post_data["post_author"], "dateCreated": self._convert_date(post_data["post_date"]), "content": content, "postid": str(post_data["ID"])})
        return struct
    # end def blogger_getpost
    #// 
    #// Retrieve list of recent posts.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type string $appkey (unused)
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $numberposts (optional)
    #// }
    #// @return array|IXR_Error
    #//
    def blogger_getrecentposts(self, args=None):
        
        self.escape(args)
        #// $args[0] = appkey - ignored.
        username = args[2]
        password = args[3]
        if (php_isset(lambda : args[4])):
            query = Array({"numberposts": absint(args[4])})
        else:
            query = Array()
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getRecentPosts")
        posts_list = wp_get_recent_posts(query)
        if (not posts_list):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(500, __("Either there are no posts, or something went wrong.")))
            return self.error
        # end if
        recent_posts = Array()
        for entry in posts_list:
            if (not current_user_can("edit_post", entry["ID"])):
                continue
            # end if
            post_date = self._convert_date(entry["post_date"])
            categories = php_implode(",", wp_get_post_categories(entry["ID"]))
            content = "<title>" + wp_unslash(entry["post_title"]) + "</title>"
            content += "<category>" + categories + "</category>"
            content += wp_unslash(entry["post_content"])
            recent_posts[-1] = Array({"userid": entry["post_author"], "dateCreated": post_date, "content": content, "postid": str(entry["ID"])})
        # end for
        return recent_posts
    # end def blogger_getrecentposts
    #// 
    #// Deprecated.
    #// 
    #// @since 1.5.0
    #// @deprecated 3.5.0
    #// 
    #// @param array $args Unused.
    #// @return IXR_Error Error object.
    #//
    def blogger_gettemplate(self, args=None):
        
        return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, this method is not supported.")))
    # end def blogger_gettemplate
    #// 
    #// Deprecated.
    #// 
    #// @since 1.5.0
    #// @deprecated 3.5.0
    #// 
    #// @param array $args Unused.
    #// @return IXR_Error Error object.
    #//
    def blogger_settemplate(self, args=None):
        
        return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, this method is not supported.")))
    # end def blogger_settemplate
    #// 
    #// Creates new post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type string $appkey (unused)
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type string $content
    #// @type string $publish
    #// }
    #// @return int|IXR_Error
    #//
    def blogger_newpost(self, args=None):
        
        self.escape(args)
        username = args[2]
        password = args[3]
        content = args[4]
        publish = args[5]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.newPost")
        cap = "publish_posts" if publish else "edit_posts"
        if (not current_user_can(get_post_type_object("post").cap.create_posts)) or (not current_user_can(cap)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to post on this site.")))
        # end if
        post_status = "publish" if publish else "draft"
        post_author = user.ID
        post_title = xmlrpc_getposttitle(content)
        post_category = xmlrpc_getpostcategory(content)
        post_content = xmlrpc_removepostdata(content)
        post_date = current_time("mysql")
        post_date_gmt = current_time("mysql", 1)
        post_data = compact("post_author", "post_date", "post_date_gmt", "post_content", "post_title", "post_category", "post_status")
        post_ID = wp_insert_post(post_data)
        if is_wp_error(post_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, post_ID.get_error_message()))
        # end if
        if (not post_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be created.")))
        # end if
        self.attach_uploads(post_ID, post_content)
        #// 
        #// Fires after a new post has been successfully created via the XML-RPC Blogger API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the new post.
        #// @param array $args    An array of new post arguments.
        #//
        do_action("xmlrpc_call_success_blogger_newPost", post_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return post_ID
    # end def blogger_newpost
    #// 
    #// Edit a post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// @type string $content
    #// @type bool   $publish
    #// }
    #// @return true|IXR_Error true when done.
    #//
    def blogger_editpost(self, args=None):
        
        self.escape(args)
        post_ID = int(args[1])
        username = args[2]
        password = args[3]
        content = args[4]
        publish = args[5]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.editPost")
        actual_post = get_post(post_ID, ARRAY_A)
        if (not actual_post) or "post" != actual_post["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
        self.escape(actual_post)
        if (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        if "publish" == actual_post["post_status"] and (not current_user_can("publish_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this post.")))
        # end if
        postdata = Array()
        postdata["ID"] = actual_post["ID"]
        postdata["post_content"] = xmlrpc_removepostdata(content)
        postdata["post_title"] = xmlrpc_getposttitle(content)
        postdata["post_category"] = xmlrpc_getpostcategory(content)
        postdata["post_status"] = actual_post["post_status"]
        postdata["post_excerpt"] = actual_post["post_excerpt"]
        postdata["post_status"] = "publish" if publish else "draft"
        result = wp_update_post(postdata)
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be updated.")))
        # end if
        self.attach_uploads(actual_post["ID"], postdata["post_content"])
        #// 
        #// Fires after a post has been successfully updated via the XML-RPC Blogger API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the updated post.
        #// @param array $args    An array of arguments for the post to edit.
        #//
        do_action("xmlrpc_call_success_blogger_editPost", post_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return True
    # end def blogger_editpost
    #// 
    #// Remove a post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// }
    #// @return true|IXR_Error True when post is deleted.
    #//
    def blogger_deletepost(self, args=None):
        
        self.escape(args)
        post_ID = int(args[1])
        username = args[2]
        password = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.deletePost")
        actual_post = get_post(post_ID, ARRAY_A)
        if (not actual_post) or "post" != actual_post["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
        if (not current_user_can("delete_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this post.")))
        # end if
        result = wp_delete_post(post_ID)
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be deleted.")))
        # end if
        #// 
        #// Fires after a post has been successfully deleted via the XML-RPC Blogger API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the deleted post.
        #// @param array $args    An array of arguments to delete the post.
        #//
        do_action("xmlrpc_call_success_blogger_deletePost", post_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return True
    # end def blogger_deletepost
    #// 
    #// MetaWeblog API functions.
    #// Specs on wherever Dave Winer wants them to be.
    #// 
    #// 
    #// Create a new post.
    #// 
    #// The 'content_struct' argument must contain:
    #// - title
    #// - description
    #// - mt_excerpt
    #// - mt_text_more
    #// - mt_keywords
    #// - mt_tb_ping_urls
    #// - categories
    #// 
    #// Also, it can optionally contain:
    #// - wp_slug
    #// - wp_password
    #// - wp_page_parent_id
    #// - wp_page_order
    #// - wp_author_id
    #// - post_status | page_status - can be 'draft', 'private', 'publish', or 'pending'
    #// - mt_allow_comments - can be 'open' or 'closed'
    #// - mt_allow_pings - can be 'open' or 'closed'
    #// - date_created_gmt
    #// - dateCreated
    #// - wp_post_thumbnail
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $content_struct
    #// @type int    $publish
    #// }
    #// @return int|IXR_Error
    #//
    def mw_newpost(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        content_struct = args[3]
        publish = args[4] if (php_isset(lambda : args[4])) else 0
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.newPost")
        page_template = ""
        if (not php_empty(lambda : content_struct["post_type"])):
            if "page" == content_struct["post_type"]:
                if publish:
                    cap = "publish_pages"
                elif (php_isset(lambda : content_struct["page_status"])) and "publish" == content_struct["page_status"]:
                    cap = "publish_pages"
                else:
                    cap = "edit_pages"
                # end if
                error_message = __("Sorry, you are not allowed to publish pages on this site.")
                post_type = "page"
                if (not php_empty(lambda : content_struct["wp_page_template"])):
                    page_template = content_struct["wp_page_template"]
                # end if
            elif "post" == content_struct["post_type"]:
                if publish:
                    cap = "publish_posts"
                elif (php_isset(lambda : content_struct["post_status"])) and "publish" == content_struct["post_status"]:
                    cap = "publish_posts"
                else:
                    cap = "edit_posts"
                # end if
                error_message = __("Sorry, you are not allowed to publish posts on this site.")
                post_type = "post"
            else:
                #// No other 'post_type' values are allowed here.
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post type.")))
            # end if
        else:
            if publish:
                cap = "publish_posts"
            elif (php_isset(lambda : content_struct["post_status"])) and "publish" == content_struct["post_status"]:
                cap = "publish_posts"
            else:
                cap = "edit_posts"
            # end if
            error_message = __("Sorry, you are not allowed to publish posts on this site.")
            post_type = "post"
        # end if
        if (not current_user_can(get_post_type_object(post_type).cap.create_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish posts on this site.")))
        # end if
        if (not current_user_can(cap)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, error_message))
        # end if
        #// Check for a valid post format if one was given.
        if (php_isset(lambda : content_struct["wp_post_format"])):
            content_struct["wp_post_format"] = sanitize_key(content_struct["wp_post_format"])
            if (not php_array_key_exists(content_struct["wp_post_format"], get_post_format_strings())):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post format.")))
            # end if
        # end if
        #// Let WordPress generate the 'post_name' (slug) unless
        #// one has been provided.
        post_name = ""
        if (php_isset(lambda : content_struct["wp_slug"])):
            post_name = content_struct["wp_slug"]
        # end if
        #// Only use a password if one was given.
        if (php_isset(lambda : content_struct["wp_password"])):
            post_password = content_struct["wp_password"]
        else:
            post_password = ""
        # end if
        #// Only set a post parent if one was given.
        if (php_isset(lambda : content_struct["wp_page_parent_id"])):
            post_parent = content_struct["wp_page_parent_id"]
        else:
            post_parent = 0
        # end if
        #// Only set the 'menu_order' if it was given.
        if (php_isset(lambda : content_struct["wp_page_order"])):
            menu_order = content_struct["wp_page_order"]
        else:
            menu_order = 0
        # end if
        post_author = user.ID
        #// If an author id was provided then use it instead.
        if (php_isset(lambda : content_struct["wp_author_id"])) and user.ID != content_struct["wp_author_id"]:
            for case in Switch(post_type):
                if case("post"):
                    if (not current_user_can("edit_others_posts")):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create posts as this user.")))
                    # end if
                    break
                # end if
                if case("page"):
                    if (not current_user_can("edit_others_pages")):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create pages as this user.")))
                    # end if
                    break
                # end if
                if case():
                    return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post type.")))
                # end if
            # end for
            author = get_userdata(content_struct["wp_author_id"])
            if (not author):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid author ID.")))
            # end if
            post_author = content_struct["wp_author_id"]
        # end if
        post_title = content_struct["title"] if (php_isset(lambda : content_struct["title"])) else None
        post_content = content_struct["description"] if (php_isset(lambda : content_struct["description"])) else None
        post_status = "publish" if publish else "draft"
        if (php_isset(lambda : content_struct[str(post_type) + str("_status")])):
            for case in Switch(content_struct[str(post_type) + str("_status")]):
                if case("draft"):
                    pass
                # end if
                if case("pending"):
                    pass
                # end if
                if case("private"):
                    pass
                # end if
                if case("publish"):
                    post_status = content_struct[str(post_type) + str("_status")]
                    break
                # end if
                if case():
                    post_status = "publish" if publish else "draft"
                    break
                # end if
            # end for
        # end if
        post_excerpt = content_struct["mt_excerpt"] if (php_isset(lambda : content_struct["mt_excerpt"])) else None
        post_more = content_struct["mt_text_more"] if (php_isset(lambda : content_struct["mt_text_more"])) else None
        tags_input = content_struct["mt_keywords"] if (php_isset(lambda : content_struct["mt_keywords"])) else None
        if (php_isset(lambda : content_struct["mt_allow_comments"])):
            if (not php_is_numeric(content_struct["mt_allow_comments"])):
                for case in Switch(content_struct["mt_allow_comments"]):
                    if case("closed"):
                        comment_status = "closed"
                        break
                    # end if
                    if case("open"):
                        comment_status = "open"
                        break
                    # end if
                    if case():
                        comment_status = get_default_comment_status(post_type)
                        break
                    # end if
                # end for
            else:
                for case in Switch(int(content_struct["mt_allow_comments"])):
                    if case(0):
                        pass
                    # end if
                    if case(2):
                        comment_status = "closed"
                        break
                    # end if
                    if case(1):
                        comment_status = "open"
                        break
                    # end if
                    if case():
                        comment_status = get_default_comment_status(post_type)
                        break
                    # end if
                # end for
            # end if
        else:
            comment_status = get_default_comment_status(post_type)
        # end if
        if (php_isset(lambda : content_struct["mt_allow_pings"])):
            if (not php_is_numeric(content_struct["mt_allow_pings"])):
                for case in Switch(content_struct["mt_allow_pings"]):
                    if case("closed"):
                        ping_status = "closed"
                        break
                    # end if
                    if case("open"):
                        ping_status = "open"
                        break
                    # end if
                    if case():
                        ping_status = get_default_comment_status(post_type, "pingback")
                        break
                    # end if
                # end for
            else:
                for case in Switch(int(content_struct["mt_allow_pings"])):
                    if case(0):
                        ping_status = "closed"
                        break
                    # end if
                    if case(1):
                        ping_status = "open"
                        break
                    # end if
                    if case():
                        ping_status = get_default_comment_status(post_type, "pingback")
                        break
                    # end if
                # end for
            # end if
        else:
            ping_status = get_default_comment_status(post_type, "pingback")
        # end if
        if post_more:
            post_content = post_content + "<!--more-->" + post_more
        # end if
        to_ping = None
        if (php_isset(lambda : content_struct["mt_tb_ping_urls"])):
            to_ping = content_struct["mt_tb_ping_urls"]
            if php_is_array(to_ping):
                to_ping = php_implode(" ", to_ping)
            # end if
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : content_struct["date_created_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated = php_rtrim(content_struct["date_created_gmt"].getiso(), "Z") + "Z"
        elif (not php_empty(lambda : content_struct["dateCreated"])):
            dateCreated = content_struct["dateCreated"].getiso()
        # end if
        if (not php_empty(lambda : dateCreated)):
            post_date = iso8601_to_datetime(dateCreated)
            post_date_gmt = iso8601_to_datetime(dateCreated, "gmt")
        else:
            post_date = ""
            post_date_gmt = ""
        # end if
        post_category = Array()
        if (php_isset(lambda : content_struct["categories"])):
            catnames = content_struct["categories"]
            if php_is_array(catnames):
                for cat in catnames:
                    post_category[-1] = get_cat_ID(cat)
                # end for
            # end if
        # end if
        postdata = compact("post_author", "post_date", "post_date_gmt", "post_content", "post_title", "post_category", "post_status", "post_excerpt", "comment_status", "ping_status", "to_ping", "post_type", "post_name", "post_password", "post_parent", "menu_order", "tags_input", "page_template")
        post_ID = get_default_post_to_edit(post_type, True).ID
        postdata["ID"] = post_ID
        #// Only posts can be sticky.
        if "post" == post_type and (php_isset(lambda : content_struct["sticky"])):
            data = postdata
            data["sticky"] = content_struct["sticky"]
            error = self._toggle_sticky(data)
            if error:
                return error
            # end if
        # end if
        if (php_isset(lambda : content_struct["custom_fields"])):
            self.set_custom_fields(post_ID, content_struct["custom_fields"])
        # end if
        if (php_isset(lambda : content_struct["wp_post_thumbnail"])):
            if set_post_thumbnail(post_ID, content_struct["wp_post_thumbnail"]) == False:
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
            # end if
            content_struct["wp_post_thumbnail"] = None
        # end if
        #// Handle enclosures.
        thisEnclosure = content_struct["enclosure"] if (php_isset(lambda : content_struct["enclosure"])) else None
        self.add_enclosure_if_new(post_ID, thisEnclosure)
        self.attach_uploads(post_ID, post_content)
        #// Handle post formats if assigned, value is validated earlier
        #// in this function.
        if (php_isset(lambda : content_struct["wp_post_format"])):
            set_post_format(post_ID, content_struct["wp_post_format"])
        # end if
        post_ID = wp_insert_post(postdata, True)
        if is_wp_error(post_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, post_ID.get_error_message()))
        # end if
        if (not post_ID):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be created.")))
        # end if
        #// 
        #// Fires after a new post has been successfully created via the XML-RPC MovableType API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the new post.
        #// @param array $args    An array of arguments to create the new post.
        #//
        do_action("xmlrpc_call_success_mw_newPost", post_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return php_strval(post_ID)
    # end def mw_newpost
    #// 
    #// Adds an enclosure to a post if it's new.
    #// 
    #// @since 2.8.0
    #// 
    #// @param integer $post_ID   Post ID.
    #// @param array   $enclosure Enclosure data.
    #//
    def add_enclosure_if_new(self, post_ID=None, enclosure=None):
        
        if php_is_array(enclosure) and (php_isset(lambda : enclosure["url"])) and (php_isset(lambda : enclosure["length"])) and (php_isset(lambda : enclosure["type"])):
            encstring = enclosure["url"] + "\n" + enclosure["length"] + "\n" + enclosure["type"] + "\n"
            found = False
            enclosures = get_post_meta(post_ID, "enclosure")
            if enclosures:
                for enc in enclosures:
                    #// This method used to omit the trailing new line. #23219
                    if php_rtrim(enc, "\n") == php_rtrim(encstring, "\n"):
                        found = True
                        break
                    # end if
                # end for
            # end if
            if (not found):
                add_post_meta(post_ID, "enclosure", encstring)
            # end if
        # end if
    # end def add_enclosure_if_new
    #// 
    #// Attach upload to a post.
    #// 
    #// @since 2.1.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $post_ID Post ID.
    #// @param string $post_content Post Content for attachment.
    #//
    def attach_uploads(self, post_ID=None, post_content=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// Find any unattached files.
        attachments = wpdb.get_results(str("SELECT ID, guid FROM ") + str(wpdb.posts) + str(" WHERE post_parent = '0' AND post_type = 'attachment'"))
        if php_is_array(attachments):
            for file in attachments:
                if (not php_empty(lambda : file.guid)) and php_strpos(post_content, file.guid) != False:
                    wpdb.update(wpdb.posts, Array({"post_parent": post_ID}), Array({"ID": file.ID}))
                # end if
            # end for
        # end if
    # end def attach_uploads
    #// 
    #// Edit a post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $content_struct
    #// @type int    $publish
    #// }
    #// @return bool|IXR_Error True on success.
    #//
    def mw_editpost(self, args=None):
        
        self.escape(args)
        post_ID = int(args[0])
        username = args[1]
        password = args[2]
        content_struct = args[3]
        publish = args[4] if (php_isset(lambda : args[4])) else 0
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.editPost")
        postdata = get_post(post_ID, ARRAY_A)
        #// 
        #// If there is no post data for the give post id, stop now and return an error.
        #// Otherwise a new post will be created (which was the old behavior).
        #//
        if (not postdata) or php_empty(lambda : postdata["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// Use wp.editPost to edit post types other than post and page.
        if (not php_in_array(postdata["post_type"], Array("post", "page"))):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post type.")))
        # end if
        #// Thwart attempt to change the post type.
        if (not php_empty(lambda : content_struct["post_type"])) and content_struct["post_type"] != postdata["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("The post type may not be changed.")))
        # end if
        #// Check for a valid post format if one was given.
        if (php_isset(lambda : content_struct["wp_post_format"])):
            content_struct["wp_post_format"] = sanitize_key(content_struct["wp_post_format"])
            if (not php_array_key_exists(content_struct["wp_post_format"], get_post_format_strings())):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post format.")))
            # end if
        # end if
        self.escape(postdata)
        ID = postdata["ID"]
        post_content = postdata["post_content"]
        post_title = postdata["post_title"]
        post_excerpt = postdata["post_excerpt"]
        post_password = postdata["post_password"]
        post_parent = postdata["post_parent"]
        post_type = postdata["post_type"]
        menu_order = postdata["menu_order"]
        ping_status = postdata["ping_status"]
        comment_status = postdata["comment_status"]
        #// Let WordPress manage slug if none was provided.
        post_name = postdata["post_name"]
        if (php_isset(lambda : content_struct["wp_slug"])):
            post_name = content_struct["wp_slug"]
        # end if
        #// Only use a password if one was given.
        if (php_isset(lambda : content_struct["wp_password"])):
            post_password = content_struct["wp_password"]
        # end if
        #// Only set a post parent if one was given.
        if (php_isset(lambda : content_struct["wp_page_parent_id"])):
            post_parent = content_struct["wp_page_parent_id"]
        # end if
        #// Only set the 'menu_order' if it was given.
        if (php_isset(lambda : content_struct["wp_page_order"])):
            menu_order = content_struct["wp_page_order"]
        # end if
        page_template = None
        if (not php_empty(lambda : content_struct["wp_page_template"])) and "page" == post_type:
            page_template = content_struct["wp_page_template"]
        # end if
        post_author = postdata["post_author"]
        #// If an author id was provided then use it instead.
        if (php_isset(lambda : content_struct["wp_author_id"])):
            #// Check permissions if attempting to switch author to or from another user.
            if user.ID != content_struct["wp_author_id"] or user.ID != post_author:
                for case in Switch(post_type):
                    if case("post"):
                        if (not current_user_can("edit_others_posts")):
                            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to change the post author as this user.")))
                        # end if
                        break
                    # end if
                    if case("page"):
                        if (not current_user_can("edit_others_pages")):
                            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to change the page author as this user.")))
                        # end if
                        break
                    # end if
                    if case():
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post type.")))
                    # end if
                # end for
                post_author = content_struct["wp_author_id"]
            # end if
        # end if
        if (php_isset(lambda : content_struct["mt_allow_comments"])):
            if (not php_is_numeric(content_struct["mt_allow_comments"])):
                for case in Switch(content_struct["mt_allow_comments"]):
                    if case("closed"):
                        comment_status = "closed"
                        break
                    # end if
                    if case("open"):
                        comment_status = "open"
                        break
                    # end if
                    if case():
                        comment_status = get_default_comment_status(post_type)
                        break
                    # end if
                # end for
            else:
                for case in Switch(int(content_struct["mt_allow_comments"])):
                    if case(0):
                        pass
                    # end if
                    if case(2):
                        comment_status = "closed"
                        break
                    # end if
                    if case(1):
                        comment_status = "open"
                        break
                    # end if
                    if case():
                        comment_status = get_default_comment_status(post_type)
                        break
                    # end if
                # end for
            # end if
        # end if
        if (php_isset(lambda : content_struct["mt_allow_pings"])):
            if (not php_is_numeric(content_struct["mt_allow_pings"])):
                for case in Switch(content_struct["mt_allow_pings"]):
                    if case("closed"):
                        ping_status = "closed"
                        break
                    # end if
                    if case("open"):
                        ping_status = "open"
                        break
                    # end if
                    if case():
                        ping_status = get_default_comment_status(post_type, "pingback")
                        break
                    # end if
                # end for
            else:
                for case in Switch(int(content_struct["mt_allow_pings"])):
                    if case(0):
                        ping_status = "closed"
                        break
                    # end if
                    if case(1):
                        ping_status = "open"
                        break
                    # end if
                    if case():
                        ping_status = get_default_comment_status(post_type, "pingback")
                        break
                    # end if
                # end for
            # end if
        # end if
        if (php_isset(lambda : content_struct["title"])):
            post_title = content_struct["title"]
        # end if
        if (php_isset(lambda : content_struct["description"])):
            post_content = content_struct["description"]
        # end if
        post_category = Array()
        if (php_isset(lambda : content_struct["categories"])):
            catnames = content_struct["categories"]
            if php_is_array(catnames):
                for cat in catnames:
                    post_category[-1] = get_cat_ID(cat)
                # end for
            # end if
        # end if
        if (php_isset(lambda : content_struct["mt_excerpt"])):
            post_excerpt = content_struct["mt_excerpt"]
        # end if
        post_more = content_struct["mt_text_more"] if (php_isset(lambda : content_struct["mt_text_more"])) else None
        post_status = "publish" if publish else "draft"
        if (php_isset(lambda : content_struct[str(post_type) + str("_status")])):
            for case in Switch(content_struct[str(post_type) + str("_status")]):
                if case("draft"):
                    pass
                # end if
                if case("pending"):
                    pass
                # end if
                if case("private"):
                    pass
                # end if
                if case("publish"):
                    post_status = content_struct[str(post_type) + str("_status")]
                    break
                # end if
                if case():
                    post_status = "publish" if publish else "draft"
                    break
                # end if
            # end for
        # end if
        tags_input = content_struct["mt_keywords"] if (php_isset(lambda : content_struct["mt_keywords"])) else None
        if "publish" == post_status or "private" == post_status:
            if "page" == post_type and (not current_user_can("publish_pages")):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this page.")))
            elif (not current_user_can("publish_posts")):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this post.")))
            # end if
        # end if
        if post_more:
            post_content = post_content + "<!--more-->" + post_more
        # end if
        to_ping = None
        if (php_isset(lambda : content_struct["mt_tb_ping_urls"])):
            to_ping = content_struct["mt_tb_ping_urls"]
            if php_is_array(to_ping):
                to_ping = php_implode(" ", to_ping)
            # end if
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : content_struct["date_created_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated = php_rtrim(content_struct["date_created_gmt"].getiso(), "Z") + "Z"
        elif (not php_empty(lambda : content_struct["dateCreated"])):
            dateCreated = content_struct["dateCreated"].getiso()
        # end if
        #// Default to not flagging the post date to be edited unless it's intentional.
        edit_date = False
        if (not php_empty(lambda : dateCreated)):
            post_date = iso8601_to_datetime(dateCreated)
            post_date_gmt = iso8601_to_datetime(dateCreated, "gmt")
            #// Flag the post date to be edited.
            edit_date = True
        else:
            post_date = postdata["post_date"]
            post_date_gmt = postdata["post_date_gmt"]
        # end if
        #// We've got all the data -- post it.
        newpost = compact("ID", "post_content", "post_title", "post_category", "post_status", "post_excerpt", "comment_status", "ping_status", "edit_date", "post_date", "post_date_gmt", "to_ping", "post_name", "post_password", "post_parent", "menu_order", "post_author", "tags_input", "page_template")
        result = wp_update_post(newpost, True)
        if is_wp_error(result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, result.get_error_message()))
        # end if
        if (not result):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be updated.")))
        # end if
        #// Only posts can be sticky.
        if "post" == post_type and (php_isset(lambda : content_struct["sticky"])):
            data = newpost
            data["sticky"] = content_struct["sticky"]
            data["post_type"] = "post"
            error = self._toggle_sticky(data, True)
            if error:
                return error
            # end if
        # end if
        if (php_isset(lambda : content_struct["custom_fields"])):
            self.set_custom_fields(post_ID, content_struct["custom_fields"])
        # end if
        if (php_isset(lambda : content_struct["wp_post_thumbnail"])):
            #// Empty value deletes, non-empty value adds/updates.
            if php_empty(lambda : content_struct["wp_post_thumbnail"]):
                delete_post_thumbnail(post_ID)
            else:
                if set_post_thumbnail(post_ID, content_struct["wp_post_thumbnail"]) == False:
                    return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
                # end if
            # end if
            content_struct["wp_post_thumbnail"] = None
        # end if
        #// Handle enclosures.
        thisEnclosure = content_struct["enclosure"] if (php_isset(lambda : content_struct["enclosure"])) else None
        self.add_enclosure_if_new(post_ID, thisEnclosure)
        self.attach_uploads(ID, post_content)
        #// Handle post formats if assigned, validation is handled earlier in this function.
        if (php_isset(lambda : content_struct["wp_post_format"])):
            set_post_format(post_ID, content_struct["wp_post_format"])
        # end if
        #// 
        #// Fires after a post has been successfully updated via the XML-RPC MovableType API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the updated post.
        #// @param array $args    An array of arguments to update the post.
        #//
        do_action("xmlrpc_call_success_mw_editPost", post_ID, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return True
    # end def mw_editpost
    #// 
    #// Retrieve post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def mw_getpost(self, args=None):
        
        self.escape(args)
        post_ID = int(args[0])
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        postdata = get_post(post_ID, ARRAY_A)
        if (not postdata):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.getPost")
        if "" != postdata["post_date"]:
            post_date = self._convert_date(postdata["post_date"])
            post_date_gmt = self._convert_date_gmt(postdata["post_date_gmt"], postdata["post_date"])
            post_modified = self._convert_date(postdata["post_modified"])
            post_modified_gmt = self._convert_date_gmt(postdata["post_modified_gmt"], postdata["post_modified"])
            categories = Array()
            catids = wp_get_post_categories(post_ID)
            for catid in catids:
                categories[-1] = get_cat_name(catid)
            # end for
            tagnames = Array()
            tags = wp_get_post_tags(post_ID)
            if (not php_empty(lambda : tags)):
                for tag in tags:
                    tagnames[-1] = tag.name
                # end for
                tagnames = php_implode(", ", tagnames)
            else:
                tagnames = ""
            # end if
            post = get_extended(postdata["post_content"])
            link = get_permalink(postdata["ID"])
            #// Get the author info.
            author = get_userdata(postdata["post_author"])
            allow_comments = 1 if "open" == postdata["comment_status"] else 0
            allow_pings = 1 if "open" == postdata["ping_status"] else 0
            #// Consider future posts as published.
            if "future" == postdata["post_status"]:
                postdata["post_status"] = "publish"
            # end if
            #// Get post format.
            post_format = get_post_format(post_ID)
            if php_empty(lambda : post_format):
                post_format = "standard"
            # end if
            sticky = False
            if is_sticky(post_ID):
                sticky = True
            # end if
            enclosure = Array()
            for key,val in get_post_custom(post_ID):
                if "enclosure" == key:
                    for enc in val:
                        encdata = php_explode("\n", enc)
                        enclosure["url"] = php_trim(htmlspecialchars(encdata[0]))
                        enclosure["length"] = int(php_trim(encdata[1]))
                        enclosure["type"] = php_trim(encdata[2])
                        break
                    # end for
                # end if
            # end for
            resp = Array({"dateCreated": post_date, "userid": postdata["post_author"], "postid": postdata["ID"], "description": post["main"], "title": postdata["post_title"], "link": link, "permaLink": link, "categories": categories, "mt_excerpt": postdata["post_excerpt"], "mt_text_more": post["extended"], "wp_more_text": post["more_text"], "mt_allow_comments": allow_comments, "mt_allow_pings": allow_pings, "mt_keywords": tagnames, "wp_slug": postdata["post_name"], "wp_password": postdata["post_password"], "wp_author_id": str(author.ID), "wp_author_display_name": author.display_name, "date_created_gmt": post_date_gmt, "post_status": postdata["post_status"], "custom_fields": self.get_custom_fields(post_ID), "wp_post_format": post_format, "sticky": sticky, "date_modified": post_modified, "date_modified_gmt": post_modified_gmt})
            if (not php_empty(lambda : enclosure)):
                resp["enclosure"] = enclosure
            # end if
            resp["wp_post_thumbnail"] = get_post_thumbnail_id(postdata["ID"])
            return resp
        else:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
    # end def mw_getpost
    #// 
    #// Retrieve list of recent posts.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $numberposts
    #// }
    #// @return array|IXR_Error
    #//
    def mw_getrecentposts(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        if (php_isset(lambda : args[3])):
            query = Array({"numberposts": absint(args[3])})
        else:
            query = Array()
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.getRecentPosts")
        posts_list = wp_get_recent_posts(query)
        if (not posts_list):
            return Array()
        # end if
        recent_posts = Array()
        for entry in posts_list:
            if (not current_user_can("edit_post", entry["ID"])):
                continue
            # end if
            post_date = self._convert_date(entry["post_date"])
            post_date_gmt = self._convert_date_gmt(entry["post_date_gmt"], entry["post_date"])
            post_modified = self._convert_date(entry["post_modified"])
            post_modified_gmt = self._convert_date_gmt(entry["post_modified_gmt"], entry["post_modified"])
            categories = Array()
            catids = wp_get_post_categories(entry["ID"])
            for catid in catids:
                categories[-1] = get_cat_name(catid)
            # end for
            tagnames = Array()
            tags = wp_get_post_tags(entry["ID"])
            if (not php_empty(lambda : tags)):
                for tag in tags:
                    tagnames[-1] = tag.name
                # end for
                tagnames = php_implode(", ", tagnames)
            else:
                tagnames = ""
            # end if
            post = get_extended(entry["post_content"])
            link = get_permalink(entry["ID"])
            #// Get the post author info.
            author = get_userdata(entry["post_author"])
            allow_comments = 1 if "open" == entry["comment_status"] else 0
            allow_pings = 1 if "open" == entry["ping_status"] else 0
            #// Consider future posts as published.
            if "future" == entry["post_status"]:
                entry["post_status"] = "publish"
            # end if
            #// Get post format.
            post_format = get_post_format(entry["ID"])
            if php_empty(lambda : post_format):
                post_format = "standard"
            # end if
            recent_posts[-1] = Array({"dateCreated": post_date, "userid": entry["post_author"], "postid": str(entry["ID"]), "description": post["main"], "title": entry["post_title"], "link": link, "permaLink": link, "categories": categories, "mt_excerpt": entry["post_excerpt"], "mt_text_more": post["extended"], "wp_more_text": post["more_text"], "mt_allow_comments": allow_comments, "mt_allow_pings": allow_pings, "mt_keywords": tagnames, "wp_slug": entry["post_name"], "wp_password": entry["post_password"], "wp_author_id": str(author.ID), "wp_author_display_name": author.display_name, "date_created_gmt": post_date_gmt, "post_status": entry["post_status"], "custom_fields": self.get_custom_fields(entry["ID"]), "wp_post_format": post_format, "date_modified": post_modified, "date_modified_gmt": post_modified_gmt, "sticky": "post" == entry["post_type"] and is_sticky(entry["ID"]), "wp_post_thumbnail": get_post_thumbnail_id(entry["ID"])})
        # end for
        return recent_posts
    # end def mw_getrecentposts
    #// 
    #// Retrieve the list of categories on a given blog.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def mw_getcategories(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view categories.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.getCategories")
        categories_struct = Array()
        cats = get_categories(Array({"get": "all"}))
        if cats:
            for cat in cats:
                struct = Array()
                struct["categoryId"] = cat.term_id
                struct["parentId"] = cat.parent
                struct["description"] = cat.name
                struct["categoryDescription"] = cat.description
                struct["categoryName"] = cat.name
                struct["htmlUrl"] = esc_html(get_category_link(cat.term_id))
                struct["rssUrl"] = esc_html(get_category_feed_link(cat.term_id, "rss2"))
                categories_struct[-1] = struct
            # end for
        # end if
        return categories_struct
    # end def mw_getcategories
    #// 
    #// Uploads a file, following your settings.
    #// 
    #// Adapted from a patch by Johann Richard.
    #// 
    #// @link http://mycvs.org/archives/2004/06/30/file-upload-to-wordpress-in-ecto
    #// 
    #// @since 1.5.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type array  $data
    #// }
    #// @return array|IXR_Error
    #//
    def mw_newmediaobject(self, args=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        username = self.escape(args[1])
        password = self.escape(args[2])
        data = args[3]
        name = sanitize_file_name(data["name"])
        type = data["type"]
        bits = data["bits"]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.newMediaObject")
        if (not current_user_can("upload_files")):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to upload files.")))
            return self.error
        # end if
        if is_multisite() and upload_is_user_over_quota(False):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(401, php_sprintf(__("Sorry, you have used your space allocation of %s. Please delete some files to upload more files."), size_format(get_space_allowed() * MB_IN_BYTES))))
            return self.error
        # end if
        #// 
        #// Filters whether to preempt the XML-RPC media upload.
        #// 
        #// Passing a truthy value will effectively short-circuit the media upload,
        #// returning that value as a 500 error instead.
        #// 
        #// @since 2.1.0
        #// 
        #// @param bool $error Whether to pre-empt the media upload. Default false.
        #//
        upload_err = apply_filters("pre_upload_error", False)
        if upload_err:
            return php_new_class("IXR_Error", lambda : IXR_Error(500, upload_err))
        # end if
        upload = wp_upload_bits(name, None, bits)
        if (not php_empty(lambda : upload["error"])):
            #// translators: 1: File name, 2: Error message.
            errorString = php_sprintf(__("Could not write file %1$s (%2$s)."), name, upload["error"])
            return php_new_class("IXR_Error", lambda : IXR_Error(500, errorString))
        # end if
        #// Construct the attachment array.
        post_id = 0
        if (not php_empty(lambda : data["post_id"])):
            post_id = int(data["post_id"])
            if (not current_user_can("edit_post", post_id)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
            # end if
        # end if
        attachment = Array({"post_title": name, "post_content": "", "post_type": "attachment", "post_parent": post_id, "post_mime_type": type, "guid": upload["url"]})
        #// Save the data.
        id = wp_insert_attachment(attachment, upload["file"], post_id)
        wp_update_attachment_metadata(id, wp_generate_attachment_metadata(id, upload["file"]))
        #// 
        #// Fires after a new attachment has been added via the XML-RPC MovableType API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $id   ID of the new attachment.
        #// @param array $args An array of arguments to add the attachment.
        #//
        do_action("xmlrpc_call_success_mw_newMediaObject", id, args)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        struct = self._prepare_media_item(get_post(id))
        #// Deprecated values.
        struct["id"] = struct["attachment_id"]
        struct["file"] = struct["title"]
        struct["url"] = struct["link"]
        return struct
    # end def mw_newmediaobject
    #// 
    #// MovableType API functions.
    #// Specs on http://www.movabletype.org/docs/mtmanual_programmatic.html
    #// 
    #// 
    #// Retrieve the post titles of recent posts.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// @type int    $numberposts
    #// }
    #// @return array|IXR_Error
    #//
    def mt_getrecentposttitles(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        if (php_isset(lambda : args[3])):
            query = Array({"numberposts": absint(args[3])})
        else:
            query = Array()
        # end if
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getRecentPostTitles")
        posts_list = wp_get_recent_posts(query)
        if (not posts_list):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(500, __("Either there are no posts, or something went wrong.")))
            return self.error
        # end if
        recent_posts = Array()
        for entry in posts_list:
            if (not current_user_can("edit_post", entry["ID"])):
                continue
            # end if
            post_date = self._convert_date(entry["post_date"])
            post_date_gmt = self._convert_date_gmt(entry["post_date_gmt"], entry["post_date"])
            recent_posts[-1] = Array({"dateCreated": post_date, "userid": entry["post_author"], "postid": str(entry["ID"]), "title": entry["post_title"], "post_status": entry["post_status"], "date_created_gmt": post_date_gmt})
        # end for
        return recent_posts
    # end def mt_getrecentposttitles
    #// 
    #// Retrieve list of all categories on blog.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $blog_id (unused)
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def mt_getcategorylist(self, args=None):
        
        self.escape(args)
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view categories.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getCategoryList")
        categories_struct = Array()
        cats = get_categories(Array({"hide_empty": 0, "hierarchical": 0}))
        if cats:
            for cat in cats:
                struct = Array()
                struct["categoryId"] = cat.term_id
                struct["categoryName"] = cat.name
                categories_struct[-1] = struct
            # end for
        # end if
        return categories_struct
    # end def mt_getcategorylist
    #// 
    #// Retrieve post categories.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// }
    #// @return array|IXR_Error
    #//
    def mt_getpostcategories(self, args=None):
        
        self.escape(args)
        post_ID = int(args[0])
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        if (not get_post(post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getPostCategories")
        categories = Array()
        catids = wp_get_post_categories(php_intval(post_ID))
        #// First listed category will be the primary category.
        isPrimary = True
        for catid in catids:
            categories[-1] = Array({"categoryName": get_cat_name(catid), "categoryId": str(catid), "isPrimary": isPrimary})
            isPrimary = False
        # end for
        return categories
    # end def mt_getpostcategories
    #// 
    #// Sets categories for a post.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// @type array  $categories
    #// }
    #// @return true|IXR_Error True on success.
    #//
    def mt_setpostcategories(self, args=None):
        
        self.escape(args)
        post_ID = int(args[0])
        username = args[1]
        password = args[2]
        categories = args[3]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.setPostCategories")
        if (not get_post(post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        catids = Array()
        for cat in categories:
            catids[-1] = cat["categoryId"]
        # end for
        wp_set_post_categories(post_ID, catids)
        return True
    # end def mt_setpostcategories
    #// 
    #// Retrieve an array of methods supported by this server.
    #// 
    #// @since 1.5.0
    #// 
    #// @return array
    #//
    def mt_supportedmethods(self):
        
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.supportedMethods")
        return php_array_keys(self.methods)
    # end def mt_supportedmethods
    #// 
    #// Retrieve an empty array because we don't support per-post text filters.
    #// 
    #// @since 1.5.0
    #//
    def mt_supportedtextfilters(self):
        
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.supportedTextFilters")
        #// 
        #// Filters the MoveableType text filters list for XML-RPC.
        #// 
        #// @since 2.2.0
        #// 
        #// @param array $filters An array of text filters.
        #//
        return apply_filters("xmlrpc_text_filters", Array())
    # end def mt_supportedtextfilters
    #// 
    #// Retrieve trackbacks sent to a given post.
    #// 
    #// @since 1.5.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param int $post_ID
    #// @return array|IXR_Error
    #//
    def mt_gettrackbackpings(self, post_ID=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getTrackbackPings")
        actual_post = get_post(post_ID, ARRAY_A)
        if (not actual_post):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
        comments = wpdb.get_results(wpdb.prepare(str("SELECT comment_author_url, comment_content, comment_author_IP, comment_type FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID = %d"), post_ID))
        if (not comments):
            return Array()
        # end if
        trackback_pings = Array()
        for comment in comments:
            if "trackback" == comment.comment_type:
                content = comment.comment_content
                title = php_substr(content, 8, php_strpos(content, "</strong>") - 8)
                trackback_pings[-1] = Array({"pingTitle": title, "pingURL": comment.comment_author_url, "pingIP": comment.comment_author_IP})
            # end if
        # end for
        return trackback_pings
    # end def mt_gettrackbackpings
    #// 
    #// Sets a post's publish status to 'publish'.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type int    $post_ID
    #// @type string $username
    #// @type string $password
    #// }
    #// @return int|IXR_Error
    #//
    def mt_publishpost(self, args=None):
        
        self.escape(args)
        post_ID = int(args[0])
        username = args[1]
        password = args[2]
        user = self.login(username, password)
        if (not user):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.publishPost")
        postdata = get_post(post_ID, ARRAY_A)
        if (not postdata):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("publish_posts")) or (not current_user_can("edit_post", post_ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this post.")))
        # end if
        postdata["post_status"] = "publish"
        #// Retain old categories.
        postdata["post_category"] = wp_get_post_categories(post_ID)
        self.escape(postdata)
        return wp_update_post(postdata)
    # end def mt_publishpost
    #// 
    #// Pingback functions.
    #// Specs on www.hixie.ch/specs/pingback/pingback
    #// 
    #// 
    #// Retrieves a pingback and registers it.
    #// 
    #// @since 1.5.0
    #// 
    #// @param array $args {
    #// Method arguments. Note: arguments must be ordered as documented.
    #// 
    #// @type string $pagelinkedfrom
    #// @type string $pagelinkedto
    #// }
    #// @return string|IXR_Error
    #//
    def pingback_ping(self, args=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "pingback.ping")
        self.escape(args)
        pagelinkedfrom = php_str_replace("&amp;", "&", args[0])
        pagelinkedto = php_str_replace("&amp;", "&", args[1])
        pagelinkedto = php_str_replace("&", "&amp;", pagelinkedto)
        #// 
        #// Filters the pingback source URI.
        #// 
        #// @since 3.6.0
        #// 
        #// @param string $pagelinkedfrom URI of the page linked from.
        #// @param string $pagelinkedto   URI of the page linked to.
        #//
        pagelinkedfrom = apply_filters("pingback_ping_source_uri", pagelinkedfrom, pagelinkedto)
        if (not pagelinkedfrom):
            return self.pingback_error(0, __("A valid URL was not provided."))
        # end if
        #// Check if the page linked to is on our site.
        pos1 = php_strpos(pagelinkedto, php_str_replace(Array("http://www.", "http://", "https://www.", "https://"), "", get_option("home")))
        if (not pos1):
            return self.pingback_error(0, __("Is there no link to us?"))
        # end if
        #// 
        #// Let's find which post is linked to.
        #// FIXME: Does url_to_postid() cover all these cases already?
        #// If so, then let's use it and drop the old code.
        #//
        urltest = php_parse_url(pagelinkedto)
        post_ID = url_to_postid(pagelinkedto)
        if post_ID:
            pass
        elif (php_isset(lambda : urltest["path"])) and php_preg_match("#p/[0-9]{1,}#", urltest["path"], match):
            #// The path defines the post_ID (archives/p/XXXX).
            blah = php_explode("/", match[0])
            post_ID = int(blah[1])
        elif (php_isset(lambda : urltest["query"])) and php_preg_match("#p=[0-9]{1,}#", urltest["query"], match):
            #// The query string defines the post_ID (?p=XXXX).
            blah = php_explode("=", match[0])
            post_ID = int(blah[1])
        elif (php_isset(lambda : urltest["fragment"])):
            #// An #anchor is there, it's either...
            if php_intval(urltest["fragment"]):
                #// ...an integer #XXXX (simplest case),
                post_ID = int(urltest["fragment"])
            elif php_preg_match("/post-[0-9]+/", urltest["fragment"]):
                #// ...a post ID in the form 'post-###',
                post_ID = php_preg_replace("/[^0-9]+/", "", urltest["fragment"])
            elif php_is_string(urltest["fragment"]):
                #// ...or a string #title, a little more complicated.
                title = php_preg_replace("/[^a-z0-9]/i", ".", urltest["fragment"])
                sql = wpdb.prepare(str("SELECT ID FROM ") + str(wpdb.posts) + str(" WHERE post_title RLIKE %s"), title)
                post_ID = wpdb.get_var(sql)
                if (not post_ID):
                    #// Returning unknown error '0' is better than die()'ing.
                    return self.pingback_error(0, "")
                # end if
            # end if
        else:
            #// TODO: Attempt to extract a post ID from the given URL.
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        post_ID = int(post_ID)
        post = get_post(post_ID)
        if (not post):
            #// Post not found.
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        if url_to_postid(pagelinkedfrom) == post_ID:
            return self.pingback_error(0, __("The source URL and the target URL cannot both point to the same resource."))
        # end if
        #// Check if pings are on.
        if (not pings_open(post)):
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        #// Let's check that the remote site didn't already pingback this entry.
        if wpdb.get_results(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID = %d AND comment_author_url = %s"), post_ID, pagelinkedfrom)):
            return self.pingback_error(48, __("The pingback has already been registered."))
        # end if
        #// Very stupid, but gives time to the 'from' server to publish!
        sleep(1)
        remote_ip = php_preg_replace("/[^0-9a-fA-F:., ]/", "", PHP_SERVER["REMOTE_ADDR"])
        #// This filter is documented in wp-includes/class-http.php
        user_agent = apply_filters("http_headers_useragent", "WordPress/" + get_bloginfo("version") + "; " + get_bloginfo("url"), pagelinkedfrom)
        #// Let's check the remote site.
        http_api_args = Array({"timeout": 10, "redirection": 0, "limit_response_size": 153600, "user-agent": str(user_agent) + str("; verifying pingback from ") + str(remote_ip), "headers": Array({"X-Pingback-Forwarded-For": remote_ip})})
        request = wp_safe_remote_get(pagelinkedfrom, http_api_args)
        remote_source = wp_remote_retrieve_body(request)
        remote_source_original = remote_source
        if (not remote_source):
            return self.pingback_error(16, __("The source URL does not exist."))
        # end if
        #// 
        #// Filters the pingback remote source.
        #// 
        #// @since 2.5.0
        #// 
        #// @param string $remote_source Response source for the page linked from.
        #// @param string $pagelinkedto  URL of the page linked to.
        #//
        remote_source = apply_filters("pre_remote_source", remote_source, pagelinkedto)
        #// Work around bug in strip_tags():
        remote_source = php_str_replace("<!DOC", "<DOC", remote_source)
        remote_source = php_preg_replace("/[\\r\\n\\t ]+/", " ", remote_source)
        #// normalize spaces
        remote_source = php_preg_replace("/<\\/*(h1|h2|h3|h4|h5|h6|p|th|td|li|dt|dd|pre|caption|input|textarea|button|body)[^>]*>/", "\n\n", remote_source)
        php_preg_match("|<title>([^<]*?)</title>|is", remote_source, matchtitle)
        title = matchtitle[1] if (php_isset(lambda : matchtitle[1])) else ""
        if php_empty(lambda : title):
            return self.pingback_error(32, __("We cannot find a title on that page."))
        # end if
        #// Remove all script and style tags including their content.
        remote_source = php_preg_replace("@<(script|style)[^>]*?>.*?</\\1>@si", "", remote_source)
        #// Just keep the tag we need.
        remote_source = strip_tags(remote_source, "<a>")
        p = php_explode("\n\n", remote_source)
        preg_target = preg_quote(pagelinkedto, "|")
        for para in p:
            if php_strpos(para, pagelinkedto) != False:
                #// It exists, but is it a link?
                php_preg_match("|<a[^>]+?" + preg_target + "[^>]*>([^>]+?)</a>|", para, context)
                #// If the URL isn't in a link context, keep looking.
                if php_empty(lambda : context):
                    continue
                # end if
                #// We're going to use this fake tag to mark the context in a bit.
                #// The marker is needed in case the link text appears more than once in the paragraph.
                excerpt = php_preg_replace("|\\</?wpcontext\\>|", "", para)
                #// prevent really long link text
                if php_strlen(context[1]) > 100:
                    context[1] = php_substr(context[1], 0, 100) + "&#8230;"
                # end if
                marker = "<wpcontext>" + context[1] + "</wpcontext>"
                #// Set up our marker.
                excerpt = php_str_replace(context[0], marker, excerpt)
                #// Swap out the link for our marker.
                excerpt = strip_tags(excerpt, "<wpcontext>")
                #// Strip all tags but our context marker.
                excerpt = php_trim(excerpt)
                preg_marker = preg_quote(marker, "|")
                excerpt = php_preg_replace(str("|.*?\\s(.{0,100}") + str(preg_marker) + str(".{0,100})\\s.*|s"), "$1", excerpt)
                excerpt = strip_tags(excerpt)
                break
            # end if
        # end for
        if php_empty(lambda : context):
            #// Link to target not found.
            return self.pingback_error(17, __("The source URL does not contain a link to the target URL, and so cannot be used as a source."))
        # end if
        pagelinkedfrom = php_str_replace("&", "&amp;", pagelinkedfrom)
        context = "[&#8230;] " + esc_html(excerpt) + " [&#8230;]"
        pagelinkedfrom = self.escape(pagelinkedfrom)
        comment_post_ID = int(post_ID)
        comment_author = title
        comment_author_email = ""
        self.escape(comment_author)
        comment_author_url = pagelinkedfrom
        comment_content = context
        self.escape(comment_content)
        comment_type = "pingback"
        commentdata = compact("comment_post_ID", "comment_author", "comment_author_url", "comment_author_email", "comment_content", "comment_type", "remote_source", "remote_source_original")
        comment_ID = wp_new_comment(commentdata)
        if is_wp_error(comment_ID):
            return self.pingback_error(0, comment_ID.get_error_message())
        # end if
        #// 
        #// Fires after a post pingback has been sent.
        #// 
        #// @since 0.71
        #// 
        #// @param int $comment_ID Comment ID.
        #//
        do_action("pingback_post", comment_ID)
        #// translators: 1: URL of the page linked from, 2: URL of the page linked to.
        return php_sprintf(__("Pingback from %1$s to %2$s registered. Keep the web talking! :-)"), pagelinkedfrom, pagelinkedto)
    # end def pingback_ping
    #// 
    #// Retrieve array of URLs that pingbacked the given URL.
    #// 
    #// Specs on http://www.aquarionics.com/misc/archives/blogite/0198.html
    #// 
    #// @since 1.5.0
    #// 
    #// @global wpdb $wpdb WordPress database abstraction object.
    #// 
    #// @param string $url
    #// @return array|IXR_Error
    #//
    def pingback_extensions_getpingbacks(self, url=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "pingback.extensions.getPingbacks")
        url = self.escape(url)
        post_ID = url_to_postid(url)
        if (not post_ID):
            #// We aren't sure that the resource is available and/or pingback enabled.
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        actual_post = get_post(post_ID, ARRAY_A)
        if (not actual_post):
            #// No such post = resource not found.
            return self.pingback_error(32, __("The specified target URL does not exist."))
        # end if
        comments = wpdb.get_results(wpdb.prepare(str("SELECT comment_author_url, comment_content, comment_author_IP, comment_type FROM ") + str(wpdb.comments) + str(" WHERE comment_post_ID = %d"), post_ID))
        if (not comments):
            return Array()
        # end if
        pingbacks = Array()
        for comment in comments:
            if "pingback" == comment.comment_type:
                pingbacks[-1] = comment.comment_author_url
            # end if
        # end for
        return pingbacks
    # end def pingback_extensions_getpingbacks
    #// 
    #// Sends a pingback error based on the given error code and message.
    #// 
    #// @since 3.6.0
    #// 
    #// @param int    $code    Error code.
    #// @param string $message Error message.
    #// @return IXR_Error Error object.
    #//
    def pingback_error(self, code=None, message=None):
        
        #// 
        #// Filters the XML-RPC pingback error return.
        #// 
        #// @since 3.5.1
        #// 
        #// @param IXR_Error $error An IXR_Error object containing the error code and message.
        #//
        return apply_filters("xmlrpc_pingback_error", php_new_class("IXR_Error", lambda : IXR_Error(code, message)))
    # end def pingback_error
# end class wp_xmlrpc_server
