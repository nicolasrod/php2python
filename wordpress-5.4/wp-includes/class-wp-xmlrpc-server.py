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
    #// 
    #// Methods.
    #// 
    #// @var array
    #//
    methods = Array()
    #// 
    #// Blog options.
    #// 
    #// @var array
    #//
    blog_options = Array()
    #// 
    #// IXR_Error instance.
    #// 
    #// @var IXR_Error
    #//
    error = Array()
    #// 
    #// Flags that the user authentication has failed in this instance of wp_xmlrpc_server.
    #// 
    #// @var bool
    #//
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
    def __call(self, name_=None, arguments_=None):
        
        
        if "_multisite_getUsersBlogs" == name_:
            return self._multisite_getusersblogs(arguments_)
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
    def addtwonumbers(self, args_=None):
        
        
        number1_ = args_[0]
        number2_ = args_[1]
        return number1_ + number2_
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
    def login(self, username_=None, password_=None):
        
        
        #// 
        #// Respect old get_option() filters left for back-compat when the 'enable_xmlrpc'
        #// option was deprecated in 3.5.0. Use the 'xmlrpc_enabled' hook instead.
        #//
        enabled_ = apply_filters("pre_option_enable_xmlrpc", False)
        if False == enabled_:
            enabled_ = apply_filters("option_enable_xmlrpc", True)
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
        enabled_ = apply_filters("xmlrpc_enabled", enabled_)
        if (not enabled_):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(405, php_sprintf(__("XML-RPC services are disabled on this site."))))
            return False
        # end if
        if self.auth_failed:
            user_ = php_new_class("WP_Error", lambda : WP_Error("login_prevented"))
        else:
            user_ = wp_authenticate(username_, password_)
        # end if
        if is_wp_error(user_):
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
            self.error = apply_filters("xmlrpc_login_error", self.error, user_)
            return False
        # end if
        wp_set_current_user(user_.ID)
        return user_
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
    def login_pass_ok(self, username_=None, password_=None):
        
        
        return php_bool(self.login(username_, password_))
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
    def escape(self, data_=None):
        
        
        if (not php_is_array(data_)):
            return wp_slash(data_)
        # end if
        for v_ in data_:
            if php_is_array(v_):
                self.escape(v_)
            elif (not php_is_object(v_)):
                v_ = wp_slash(v_)
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
    def get_custom_fields(self, post_id_=None):
        
        
        post_id_ = php_int(post_id_)
        custom_fields_ = Array()
        for meta_ in has_meta(post_id_):
            #// Don't expose protected fields.
            if (not current_user_can("edit_post_meta", post_id_, meta_["meta_key"])):
                continue
            # end if
            custom_fields_[-1] = Array({"id": meta_["meta_id"], "key": meta_["meta_key"], "value": meta_["meta_value"]})
        # end for
        return custom_fields_
    # end def get_custom_fields
    #// 
    #// Set custom fields for post.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int $post_id Post ID.
    #// @param array $fields Custom fields.
    #//
    def set_custom_fields(self, post_id_=None, fields_=None):
        
        
        post_id_ = php_int(post_id_)
        for meta_ in fields_:
            if (php_isset(lambda : meta_["id"])):
                meta_["id"] = php_int(meta_["id"])
                pmeta_ = get_metadata_by_mid("post", meta_["id"])
                if (not pmeta_) or pmeta_.post_id != post_id_:
                    continue
                # end if
                if (php_isset(lambda : meta_["key"])):
                    meta_["key"] = wp_unslash(meta_["key"])
                    if meta_["key"] != pmeta_.meta_key:
                        continue
                    # end if
                    meta_["value"] = wp_unslash(meta_["value"])
                    if current_user_can("edit_post_meta", post_id_, meta_["key"]):
                        update_metadata_by_mid("post", meta_["id"], meta_["value"])
                    # end if
                elif current_user_can("delete_post_meta", post_id_, pmeta_.meta_key):
                    delete_metadata_by_mid("post", meta_["id"])
                # end if
            elif current_user_can("add_post_meta", post_id_, wp_unslash(meta_["key"])):
                add_post_meta(post_id_, meta_["key"], meta_["value"])
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
    def get_term_custom_fields(self, term_id_=None):
        
        
        term_id_ = php_int(term_id_)
        custom_fields_ = Array()
        for meta_ in has_term_meta(term_id_):
            if (not current_user_can("edit_term_meta", term_id_)):
                continue
            # end if
            custom_fields_[-1] = Array({"id": meta_["meta_id"], "key": meta_["meta_key"], "value": meta_["meta_value"]})
        # end for
        return custom_fields_
    # end def get_term_custom_fields
    #// 
    #// Set custom fields for a term.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $term_id Term ID.
    #// @param array $fields Custom fields.
    #//
    def set_term_custom_fields(self, term_id_=None, fields_=None):
        
        
        term_id_ = php_int(term_id_)
        for meta_ in fields_:
            if (php_isset(lambda : meta_["id"])):
                meta_["id"] = php_int(meta_["id"])
                pmeta_ = get_metadata_by_mid("term", meta_["id"])
                if (php_isset(lambda : meta_["key"])):
                    meta_["key"] = wp_unslash(meta_["key"])
                    if meta_["key"] != pmeta_.meta_key:
                        continue
                    # end if
                    meta_["value"] = wp_unslash(meta_["value"])
                    if current_user_can("edit_term_meta", term_id_):
                        update_metadata_by_mid("term", meta_["id"], meta_["value"])
                    # end if
                elif current_user_can("delete_term_meta", term_id_):
                    delete_metadata_by_mid("term", meta_["id"])
                # end if
            elif current_user_can("add_term_meta", term_id_):
                add_term_meta(term_id_, meta_["key"], meta_["value"])
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
    def wp_getusersblogs(self, args_=None):
        
        
        if (not self.minimum_args(args_, 2)):
            return self.error
        # end if
        #// If this isn't on WPMU then just use blogger_getUsersBlogs().
        if (not is_multisite()):
            array_unshift(args_, 1)
            return self.blogger_getusersblogs(args_)
        # end if
        self.escape(args_)
        username_ = args_[0]
        password_ = args_[1]
        user_ = self.login(username_, password_)
        if (not user_):
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
        blogs_ = get_blogs_of_user(user_.ID)
        struct_ = Array()
        primary_blog_id_ = 0
        active_blog_ = get_active_blog_for_user(user_.ID)
        if active_blog_:
            primary_blog_id_ = php_int(active_blog_.blog_id)
        # end if
        for blog_ in blogs_:
            #// Don't include blogs that aren't hosted at this site.
            if get_current_network_id() != blog_.site_id:
                continue
            # end if
            blog_id_ = blog_.userblog_id
            switch_to_blog(blog_id_)
            is_admin_ = current_user_can("manage_options")
            is_primary_ = php_int(blog_id_) == primary_blog_id_
            struct_[-1] = Array({"isAdmin": is_admin_, "isPrimary": is_primary_, "url": home_url("/"), "blogid": php_str(blog_id_), "blogName": get_option("blogname"), "xmlrpc": site_url("xmlrpc.php", "rpc")})
            restore_current_blog()
        # end for
        return struct_
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
    def minimum_args(self, args_=None, count_=None):
        
        
        if (not php_is_array(args_)) or php_count(args_) < count_:
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
    def _prepare_taxonomy(self, taxonomy_=None, fields_=None):
        
        
        _taxonomy_ = Array({"name": taxonomy_.name, "label": taxonomy_.label, "hierarchical": php_bool(taxonomy_.hierarchical), "public": php_bool(taxonomy_.public), "show_ui": php_bool(taxonomy_.show_ui), "_builtin": php_bool(taxonomy_._builtin)})
        if php_in_array("labels", fields_):
            _taxonomy_["labels"] = taxonomy_.labels
        # end if
        if php_in_array("cap", fields_):
            _taxonomy_["cap"] = taxonomy_.cap
        # end if
        if php_in_array("menu", fields_):
            _taxonomy_["show_in_menu"] = php_bool(_taxonomy_.show_in_menu)
        # end if
        if php_in_array("object_type", fields_):
            _taxonomy_["object_type"] = array_unique(taxonomy_.object_type)
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
        return apply_filters("xmlrpc_prepare_taxonomy", _taxonomy_, taxonomy_, fields_)
    # end def _prepare_taxonomy
    #// 
    #// Prepares term data for return in an XML-RPC object.
    #// 
    #// @param array|object $term The unprepared term data.
    #// @return array The prepared term data.
    #//
    def _prepare_term(self, term_=None):
        
        
        _term_ = term_
        if (not php_is_array(_term_)):
            _term_ = get_object_vars(_term_)
        # end if
        #// For integers which may be larger than XML-RPC supports ensure we return strings.
        _term_["term_id"] = php_strval(_term_["term_id"])
        _term_["term_group"] = php_strval(_term_["term_group"])
        _term_["term_taxonomy_id"] = php_strval(_term_["term_taxonomy_id"])
        _term_["parent"] = php_strval(_term_["parent"])
        #// Count we are happy to return as an integer because people really shouldn't use terms that much.
        _term_["count"] = php_intval(_term_["count"])
        #// Get term meta.
        _term_["custom_fields"] = self.get_term_custom_fields(_term_["term_id"])
        #// 
        #// Filters XML-RPC-prepared data for the given term.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array        $_term An array of term data.
        #// @param array|object $term  Term object or array.
        #//
        return apply_filters("xmlrpc_prepare_term", _term_, term_)
    # end def _prepare_term
    #// 
    #// Convert a WordPress date string to an IXR_Date object.
    #// 
    #// @param string $date Date string to convert.
    #// @return IXR_Date IXR_Date object.
    #//
    def _convert_date(self, date_=None):
        
        
        if "0000-00-00 00:00:00" == date_:
            return php_new_class("IXR_Date", lambda : IXR_Date("00000000T00:00:00Z"))
        # end if
        return php_new_class("IXR_Date", lambda : IXR_Date(mysql2date("Ymd\\TH:i:s", date_, False)))
    # end def _convert_date
    #// 
    #// Convert a WordPress GMT date string to an IXR_Date object.
    #// 
    #// @param string $date_gmt WordPress GMT date string.
    #// @param string $date     Date string.
    #// @return IXR_Date IXR_Date object.
    #//
    def _convert_date_gmt(self, date_gmt_=None, date_=None):
        
        
        if "0000-00-00 00:00:00" != date_ and "0000-00-00 00:00:00" == date_gmt_:
            return php_new_class("IXR_Date", lambda : IXR_Date(get_gmt_from_date(mysql2date("Y-m-d H:i:s", date_, False), "Ymd\\TH:i:s")))
        # end if
        return self._convert_date(date_gmt_)
    # end def _convert_date_gmt
    #// 
    #// Prepares post data for return in an XML-RPC object.
    #// 
    #// @param array $post   The unprepared post data.
    #// @param array $fields The subset of post type fields to return.
    #// @return array The prepared post data.
    #//
    def _prepare_post(self, post_=None, fields_=None):
        
        
        #// Holds the data for this post. built up based on $fields.
        _post_ = Array({"post_id": php_strval(post_["ID"])})
        #// Prepare common post fields.
        post_fields_ = Array({"post_title": post_["post_title"], "post_date": self._convert_date(post_["post_date"]), "post_date_gmt": self._convert_date_gmt(post_["post_date_gmt"], post_["post_date"]), "post_modified": self._convert_date(post_["post_modified"]), "post_modified_gmt": self._convert_date_gmt(post_["post_modified_gmt"], post_["post_modified"]), "post_status": post_["post_status"], "post_type": post_["post_type"], "post_name": post_["post_name"], "post_author": post_["post_author"], "post_password": post_["post_password"], "post_excerpt": post_["post_excerpt"], "post_content": post_["post_content"], "post_parent": php_strval(post_["post_parent"]), "post_mime_type": post_["post_mime_type"], "link": get_permalink(post_["ID"]), "guid": post_["guid"], "menu_order": php_intval(post_["menu_order"]), "comment_status": post_["comment_status"], "ping_status": post_["ping_status"], "sticky": "post" == post_["post_type"] and is_sticky(post_["ID"])})
        #// Thumbnail.
        post_fields_["post_thumbnail"] = Array()
        thumbnail_id_ = get_post_thumbnail_id(post_["ID"])
        if thumbnail_id_:
            thumbnail_size_ = "post-thumbnail" if current_theme_supports("post-thumbnail") else "thumbnail"
            post_fields_["post_thumbnail"] = self._prepare_media_item(get_post(thumbnail_id_), thumbnail_size_)
        # end if
        #// Consider future posts as published.
        if "future" == post_fields_["post_status"]:
            post_fields_["post_status"] = "publish"
        # end if
        #// Fill in blank post format.
        post_fields_["post_format"] = get_post_format(post_["ID"])
        if php_empty(lambda : post_fields_["post_format"]):
            post_fields_["post_format"] = "standard"
        # end if
        #// Merge requested $post_fields fields into $_post.
        if php_in_array("post", fields_):
            _post_ = php_array_merge(_post_, post_fields_)
        else:
            requested_fields_ = php_array_intersect_key(post_fields_, php_array_flip(fields_))
            _post_ = php_array_merge(_post_, requested_fields_)
        # end if
        all_taxonomy_fields_ = php_in_array("taxonomies", fields_)
        if all_taxonomy_fields_ or php_in_array("terms", fields_):
            post_type_taxonomies_ = get_object_taxonomies(post_["post_type"], "names")
            terms_ = wp_get_object_terms(post_["ID"], post_type_taxonomies_)
            _post_["terms"] = Array()
            for term_ in terms_:
                _post_["terms"][-1] = self._prepare_term(term_)
            # end for
        # end if
        if php_in_array("custom_fields", fields_):
            _post_["custom_fields"] = self.get_custom_fields(post_["ID"])
        # end if
        if php_in_array("enclosure", fields_):
            _post_["enclosure"] = Array()
            enclosures_ = get_post_meta(post_["ID"], "enclosure")
            if (not php_empty(lambda : enclosures_)):
                encdata_ = php_explode("\n", enclosures_[0])
                _post_["enclosure"]["url"] = php_trim(htmlspecialchars(encdata_[0]))
                _post_["enclosure"]["length"] = php_int(php_trim(encdata_[1]))
                _post_["enclosure"]["type"] = php_trim(encdata_[2])
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
        return apply_filters("xmlrpc_prepare_post", _post_, post_, fields_)
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
    def _prepare_post_type(self, post_type_=None, fields_=None):
        
        
        _post_type_ = Array({"name": post_type_.name, "label": post_type_.label, "hierarchical": php_bool(post_type_.hierarchical), "public": php_bool(post_type_.public), "show_ui": php_bool(post_type_.show_ui), "_builtin": php_bool(post_type_._builtin), "has_archive": php_bool(post_type_.has_archive), "supports": get_all_post_type_supports(post_type_.name)})
        if php_in_array("labels", fields_):
            _post_type_["labels"] = post_type_.labels
        # end if
        if php_in_array("cap", fields_):
            _post_type_["cap"] = post_type_.cap
            _post_type_["map_meta_cap"] = php_bool(post_type_.map_meta_cap)
        # end if
        if php_in_array("menu", fields_):
            _post_type_["menu_position"] = php_int(post_type_.menu_position)
            _post_type_["menu_icon"] = post_type_.menu_icon
            _post_type_["show_in_menu"] = php_bool(post_type_.show_in_menu)
        # end if
        if php_in_array("taxonomies", fields_):
            _post_type_["taxonomies"] = get_object_taxonomies(post_type_.name, "names")
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
        return apply_filters("xmlrpc_prepare_post_type", _post_type_, post_type_)
    # end def _prepare_post_type
    #// 
    #// Prepares media item data for return in an XML-RPC object.
    #// 
    #// @param object $media_item     The unprepared media item data.
    #// @param string $thumbnail_size The image size to use for the thumbnail URL.
    #// @return array The prepared media item data.
    #//
    def _prepare_media_item(self, media_item_=None, thumbnail_size_="thumbnail"):
        
        
        _media_item_ = Array({"attachment_id": php_strval(media_item_.ID), "date_created_gmt": self._convert_date_gmt(media_item_.post_date_gmt, media_item_.post_date), "parent": media_item_.post_parent, "link": wp_get_attachment_url(media_item_.ID), "title": media_item_.post_title, "caption": media_item_.post_excerpt, "description": media_item_.post_content, "metadata": wp_get_attachment_metadata(media_item_.ID), "type": media_item_.post_mime_type})
        thumbnail_src_ = image_downsize(media_item_.ID, thumbnail_size_)
        if thumbnail_src_:
            _media_item_["thumbnail"] = thumbnail_src_[0]
        else:
            _media_item_["thumbnail"] = _media_item_["link"]
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
        return apply_filters("xmlrpc_prepare_media_item", _media_item_, media_item_, thumbnail_size_)
    # end def _prepare_media_item
    #// 
    #// Prepares page data for return in an XML-RPC object.
    #// 
    #// @param object $page The unprepared page data.
    #// @return array The prepared page data.
    #//
    def _prepare_page(self, page_=None):
        
        
        #// Get all of the page content and link.
        full_page_ = get_extended(page_.post_content)
        link_ = get_permalink(page_.ID)
        #// Get info the page parent if there is one.
        parent_title_ = ""
        if (not php_empty(lambda : page_.post_parent)):
            parent_ = get_post(page_.post_parent)
            parent_title_ = parent_.post_title
        # end if
        #// Determine comment and ping settings.
        allow_comments_ = 1 if comments_open(page_.ID) else 0
        allow_pings_ = 1 if pings_open(page_.ID) else 0
        #// Format page date.
        page_date_ = self._convert_date(page_.post_date)
        page_date_gmt_ = self._convert_date_gmt(page_.post_date_gmt, page_.post_date)
        #// Pull the categories info together.
        categories_ = Array()
        if is_object_in_taxonomy("page", "category"):
            for cat_id_ in wp_get_post_categories(page_.ID):
                categories_[-1] = get_cat_name(cat_id_)
            # end for
        # end if
        #// Get the author info.
        author_ = get_userdata(page_.post_author)
        page_template_ = get_page_template_slug(page_.ID)
        if php_empty(lambda : page_template_):
            page_template_ = "default"
        # end if
        _page_ = Array({"dateCreated": page_date_, "userid": page_.post_author, "page_id": page_.ID, "page_status": page_.post_status, "description": full_page_["main"], "title": page_.post_title, "link": link_, "permaLink": link_, "categories": categories_, "excerpt": page_.post_excerpt, "text_more": full_page_["extended"], "mt_allow_comments": allow_comments_, "mt_allow_pings": allow_pings_, "wp_slug": page_.post_name, "wp_password": page_.post_password, "wp_author": author_.display_name, "wp_page_parent_id": page_.post_parent, "wp_page_parent_title": parent_title_, "wp_page_order": page_.menu_order, "wp_author_id": php_str(author_.ID), "wp_author_display_name": author_.display_name, "date_created_gmt": page_date_gmt_, "custom_fields": self.get_custom_fields(page_.ID), "wp_page_template": page_template_})
        #// 
        #// Filters XML-RPC-prepared data for the given page.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array   $_page An array of page data.
        #// @param WP_Post $page  Page object.
        #//
        return apply_filters("xmlrpc_prepare_page", _page_, page_)
    # end def _prepare_page
    #// 
    #// Prepares comment data for return in an XML-RPC object.
    #// 
    #// @param object $comment The unprepared comment data.
    #// @return array The prepared comment data.
    #//
    def _prepare_comment(self, comment_=None):
        
        
        #// Format page date.
        comment_date_gmt_ = self._convert_date_gmt(comment_.comment_date_gmt, comment_.comment_date)
        if "0" == comment_.comment_approved:
            comment_status_ = "hold"
        elif "spam" == comment_.comment_approved:
            comment_status_ = "spam"
        elif "1" == comment_.comment_approved:
            comment_status_ = "approve"
        else:
            comment_status_ = comment_.comment_approved
        # end if
        _comment_ = Array({"date_created_gmt": comment_date_gmt_, "user_id": comment_.user_id, "comment_id": comment_.comment_ID, "parent": comment_.comment_parent, "status": comment_status_, "content": comment_.comment_content, "link": get_comment_link(comment_), "post_id": comment_.comment_post_ID, "post_title": get_the_title(comment_.comment_post_ID), "author": comment_.comment_author, "author_url": comment_.comment_author_url, "author_email": comment_.comment_author_email, "author_ip": comment_.comment_author_IP, "type": comment_.comment_type})
        #// 
        #// Filters XML-RPC-prepared data for the given comment.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array      $_comment An array of prepared comment data.
        #// @param WP_Comment $comment  Comment object.
        #//
        return apply_filters("xmlrpc_prepare_comment", _comment_, comment_)
    # end def _prepare_comment
    #// 
    #// Prepares user data for return in an XML-RPC object.
    #// 
    #// @param WP_User $user   The unprepared user object.
    #// @param array   $fields The subset of user fields to return.
    #// @return array The prepared user data.
    #//
    def _prepare_user(self, user_=None, fields_=None):
        
        
        _user_ = Array({"user_id": php_strval(user_.ID)})
        user_fields_ = Array({"username": user_.user_login, "first_name": user_.user_firstname, "last_name": user_.user_lastname, "registered": self._convert_date(user_.user_registered), "bio": user_.user_description, "email": user_.user_email, "nickname": user_.nickname, "nicename": user_.user_nicename, "url": user_.user_url, "display_name": user_.display_name, "roles": user_.roles})
        if php_in_array("all", fields_):
            _user_ = php_array_merge(_user_, user_fields_)
        else:
            if php_in_array("basic", fields_):
                basic_fields_ = Array("username", "email", "registered", "display_name", "nicename")
                fields_ = php_array_merge(fields_, basic_fields_)
            # end if
            requested_fields_ = php_array_intersect_key(user_fields_, php_array_flip(fields_))
            _user_ = php_array_merge(_user_, requested_fields_)
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
        return apply_filters("xmlrpc_prepare_user", _user_, user_, fields_)
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
    def wp_newpost(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        content_struct_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// Convert the date field back to IXR form.
        if (php_isset(lambda : content_struct_["post_date"])) and (not type(content_struct_["post_date"]).__name__ == "IXR_Date"):
            content_struct_["post_date"] = self._convert_date(content_struct_["post_date"])
        # end if
        #// 
        #// Ignore the existing GMT date if it is empty or a non-GMT date was supplied in $content_struct,
        #// since _insert_post() will ignore the non-GMT date if the GMT date is set.
        #//
        if (php_isset(lambda : content_struct_["post_date_gmt"])) and (not type(content_struct_["post_date_gmt"]).__name__ == "IXR_Date"):
            if "0000-00-00 00:00:00" == content_struct_["post_date_gmt"] or (php_isset(lambda : content_struct_["post_date"])):
                content_struct_["post_date_gmt"] = None
            else:
                content_struct_["post_date_gmt"] = self._convert_date(content_struct_["post_date_gmt"])
            # end if
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newPost")
        content_struct_["ID"] = None
        return self._insert_post(user_, content_struct_)
    # end def wp_newpost
    #// 
    #// Helper method for filtering out elements from an array.
    #// 
    #// @since 3.4.0
    #// 
    #// @param int $count Number to compare to one.
    #//
    def _is_greater_than_one(self, count_=None):
        
        
        return count_ > 1
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
    def _toggle_sticky(self, post_data_=None, update_=None):
        if update_ is None:
            update_ = False
        # end if
        
        post_type_ = get_post_type_object(post_data_["post_type"])
        #// Private and password-protected posts cannot be stickied.
        if "private" == post_data_["post_status"] or (not php_empty(lambda : post_data_["post_password"])):
            #// Error if the client tried to stick the post, otherwise, silently unstick.
            if (not php_empty(lambda : post_data_["sticky"])):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you cannot stick a private post.")))
            # end if
            if update_:
                unstick_post(post_data_["ID"])
            # end if
        elif (php_isset(lambda : post_data_["sticky"])):
            if (not current_user_can(post_type_.cap.edit_others_posts)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to make posts sticky.")))
            # end if
            sticky_ = wp_validate_boolean(post_data_["sticky"])
            if sticky_:
                stick_post(post_data_["ID"])
            else:
                unstick_post(post_data_["ID"])
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
    def _insert_post(self, user_=None, content_struct_=None):
        
        
        defaults_ = Array({"post_status": "draft", "post_type": "post", "post_author": None, "post_password": None, "post_excerpt": None, "post_content": None, "post_title": None, "post_date": None, "post_date_gmt": None, "post_format": None, "post_name": None, "post_thumbnail": None, "post_parent": None, "ping_status": None, "comment_status": None, "custom_fields": None, "terms_names": None, "terms": None, "sticky": None, "enclosure": None, "ID": None})
        post_data_ = wp_parse_args(php_array_intersect_key(content_struct_, defaults_), defaults_)
        post_type_ = get_post_type_object(post_data_["post_type"])
        if (not post_type_):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid post type.")))
        # end if
        update_ = (not php_empty(lambda : post_data_["ID"]))
        if update_:
            if (not get_post(post_data_["ID"])):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post ID.")))
            # end if
            if (not current_user_can("edit_post", post_data_["ID"])):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
            # end if
            if get_post_type(post_data_["ID"]) != post_data_["post_type"]:
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("The post type may not be changed.")))
            # end if
        else:
            if (not current_user_can(post_type_.cap.create_posts)) or (not current_user_can(post_type_.cap.edit_posts)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to post on this site.")))
            # end if
        # end if
        for case in Switch(post_data_["post_status"]):
            if case("draft"):
                pass
            # end if
            if case("pending"):
                break
            # end if
            if case("private"):
                if (not current_user_can(post_type_.cap.publish_posts)):
                    return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create private posts in this post type.")))
                # end if
                break
            # end if
            if case("publish"):
                pass
            # end if
            if case("future"):
                if (not current_user_can(post_type_.cap.publish_posts)):
                    return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish posts in this post type.")))
                # end if
                break
            # end if
            if case():
                if (not get_post_status_object(post_data_["post_status"])):
                    post_data_["post_status"] = "draft"
                # end if
                break
            # end if
        # end for
        if (not php_empty(lambda : post_data_["post_password"])) and (not current_user_can(post_type_.cap.publish_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create password protected posts in this post type.")))
        # end if
        post_data_["post_author"] = absint(post_data_["post_author"])
        if (not php_empty(lambda : post_data_["post_author"])) and post_data_["post_author"] != user_.ID:
            if (not current_user_can(post_type_.cap.edit_others_posts)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create posts as this user.")))
            # end if
            author_ = get_userdata(post_data_["post_author"])
            if (not author_):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid author ID.")))
            # end if
        else:
            post_data_["post_author"] = user_.ID
        # end if
        if (php_isset(lambda : post_data_["comment_status"])) and "open" != post_data_["comment_status"] and "closed" != post_data_["comment_status"]:
            post_data_["comment_status"] = None
        # end if
        if (php_isset(lambda : post_data_["ping_status"])) and "open" != post_data_["ping_status"] and "closed" != post_data_["ping_status"]:
            post_data_["ping_status"] = None
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : post_data_["post_date_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated_ = php_rtrim(post_data_["post_date_gmt"].getiso(), "Z") + "Z"
        elif (not php_empty(lambda : post_data_["post_date"])):
            dateCreated_ = post_data_["post_date"].getiso()
        # end if
        #// Default to not flagging the post date to be edited unless it's intentional.
        post_data_["edit_date"] = False
        if (not php_empty(lambda : dateCreated_)):
            post_data_["post_date"] = iso8601_to_datetime(dateCreated_)
            post_data_["post_date_gmt"] = iso8601_to_datetime(dateCreated_, "gmt")
            #// Flag the post date to be edited.
            post_data_["edit_date"] = True
        # end if
        if (not (php_isset(lambda : post_data_["ID"]))):
            post_data_["ID"] = get_default_post_to_edit(post_data_["post_type"], True).ID
        # end if
        post_ID_ = post_data_["ID"]
        if "post" == post_data_["post_type"]:
            error_ = self._toggle_sticky(post_data_, update_)
            if error_:
                return error_
            # end if
        # end if
        if (php_isset(lambda : post_data_["post_thumbnail"])):
            #// Empty value deletes, non-empty value adds/updates.
            if (not post_data_["post_thumbnail"]):
                delete_post_thumbnail(post_ID_)
            elif (not get_post(absint(post_data_["post_thumbnail"]))):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
            # end if
            set_post_thumbnail(post_ID_, post_data_["post_thumbnail"])
            content_struct_["post_thumbnail"] = None
        # end if
        if (php_isset(lambda : post_data_["custom_fields"])):
            self.set_custom_fields(post_ID_, post_data_["custom_fields"])
        # end if
        if (php_isset(lambda : post_data_["terms"])) or (php_isset(lambda : post_data_["terms_names"])):
            post_type_taxonomies_ = get_object_taxonomies(post_data_["post_type"], "objects")
            #// Accumulate term IDs from terms and terms_names.
            terms_ = Array()
            #// First validate the terms specified by ID.
            if (php_isset(lambda : post_data_["terms"])) and php_is_array(post_data_["terms"]):
                taxonomies_ = php_array_keys(post_data_["terms"])
                #// Validating term ids.
                for taxonomy_ in taxonomies_:
                    if (not php_array_key_exists(taxonomy_, post_type_taxonomies_)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, one of the given taxonomies is not supported by the post type.")))
                    # end if
                    if (not current_user_can(post_type_taxonomies_[taxonomy_].cap.assign_terms)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign a term to one of the given taxonomies.")))
                    # end if
                    term_ids_ = post_data_["terms"][taxonomy_]
                    terms_[taxonomy_] = Array()
                    for term_id_ in term_ids_:
                        term_ = get_term_by("id", term_id_, taxonomy_)
                        if (not term_):
                            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid term ID.")))
                        # end if
                        terms_[taxonomy_][-1] = php_int(term_id_)
                    # end for
                # end for
            # end if
            #// Now validate terms specified by name.
            if (php_isset(lambda : post_data_["terms_names"])) and php_is_array(post_data_["terms_names"]):
                taxonomies_ = php_array_keys(post_data_["terms_names"])
                for taxonomy_ in taxonomies_:
                    if (not php_array_key_exists(taxonomy_, post_type_taxonomies_)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, one of the given taxonomies is not supported by the post type.")))
                    # end if
                    if (not current_user_can(post_type_taxonomies_[taxonomy_].cap.assign_terms)):
                        return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign a term to one of the given taxonomies.")))
                    # end if
                    #// 
                    #// For hierarchical taxonomies, we can't assign a term when multiple terms
                    #// in the hierarchy share the same name.
                    #//
                    ambiguous_terms_ = Array()
                    if is_taxonomy_hierarchical(taxonomy_):
                        tax_term_names_ = get_terms(Array({"taxonomy": taxonomy_, "fields": "names", "hide_empty": False}))
                        #// Count the number of terms with the same name.
                        tax_term_names_count_ = php_array_count_values(tax_term_names_)
                        #// Filter out non-ambiguous term names.
                        ambiguous_tax_term_counts_ = php_array_filter(tax_term_names_count_, Array(self, "_is_greater_than_one"))
                        ambiguous_terms_ = php_array_keys(ambiguous_tax_term_counts_)
                    # end if
                    term_names_ = post_data_["terms_names"][taxonomy_]
                    for term_name_ in term_names_:
                        if php_in_array(term_name_, ambiguous_terms_):
                            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Ambiguous term name used in a hierarchical taxonomy. Please use term ID instead.")))
                        # end if
                        term_ = get_term_by("name", term_name_, taxonomy_)
                        if (not term_):
                            #// Term doesn't exist, so check that the user is allowed to create new terms.
                            if (not current_user_can(post_type_taxonomies_[taxonomy_].cap.edit_terms)):
                                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to add a term to one of the given taxonomies.")))
                            # end if
                            #// Create the new term.
                            term_info_ = wp_insert_term(term_name_, taxonomy_)
                            if is_wp_error(term_info_):
                                return php_new_class("IXR_Error", lambda : IXR_Error(500, term_info_.get_error_message()))
                            # end if
                            terms_[taxonomy_][-1] = php_int(term_info_["term_id"])
                        else:
                            terms_[taxonomy_][-1] = php_int(term_.term_id)
                        # end if
                    # end for
                # end for
            # end if
            post_data_["tax_input"] = terms_
            post_data_["terms"] = None
            post_data_["terms_names"] = None
        # end if
        if (php_isset(lambda : post_data_["post_format"])):
            format_ = set_post_format(post_ID_, post_data_["post_format"])
            if is_wp_error(format_):
                return php_new_class("IXR_Error", lambda : IXR_Error(500, format_.get_error_message()))
            # end if
            post_data_["post_format"] = None
        # end if
        #// Handle enclosures.
        enclosure_ = post_data_["enclosure"] if (php_isset(lambda : post_data_["enclosure"])) else None
        self.add_enclosure_if_new(post_ID_, enclosure_)
        self.attach_uploads(post_ID_, post_data_["post_content"])
        #// 
        #// Filters post data array to be inserted via XML-RPC.
        #// 
        #// @since 3.4.0
        #// 
        #// @param array $post_data      Parsed array of post data.
        #// @param array $content_struct Post data array.
        #//
        post_data_ = apply_filters("xmlrpc_wp_insert_post_data", post_data_, content_struct_)
        post_ID_ = wp_update_post(post_data_, True) if update_ else wp_insert_post(post_data_, True)
        if is_wp_error(post_ID_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, post_ID_.get_error_message()))
        # end if
        if (not post_ID_):
            if update_:
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, the post could not be updated.")))
            else:
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, the post could not be created.")))
            # end if
        # end if
        return php_strval(post_ID_)
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
    def wp_editpost(self, args_=None):
        
        
        if (not self.minimum_args(args_, 5)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_id_ = php_int(args_[3])
        content_struct_ = args_[4]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editPost")
        post_ = get_post(post_id_, ARRAY_A)
        if php_empty(lambda : post_["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (php_isset(lambda : content_struct_["if_not_modified_since"])):
            #// If the post has been modified since the date provided, return an error.
            if mysql2date("U", post_["post_modified_gmt"]) > content_struct_["if_not_modified_since"].gettimestamp():
                return php_new_class("IXR_Error", lambda : IXR_Error(409, __("There is a revision of this post that is more recent.")))
            # end if
        # end if
        #// Convert the date field back to IXR form.
        post_["post_date"] = self._convert_date(post_["post_date"])
        #// 
        #// Ignore the existing GMT date if it is empty or a non-GMT date was supplied in $content_struct,
        #// since _insert_post() will ignore the non-GMT date if the GMT date is set.
        #//
        if "0000-00-00 00:00:00" == post_["post_date_gmt"] or (php_isset(lambda : content_struct_["post_date"])):
            post_["post_date_gmt"] = None
        else:
            post_["post_date_gmt"] = self._convert_date(post_["post_date_gmt"])
        # end if
        #// 
        #// If the API client did not provide 'post_date', then we must not perpetuate the value that
        #// was stored in the database, or it will appear to be an intentional edit. Conveying it here
        #// as if it was coming from the API client will cause an otherwise zeroed out 'post_date_gmt'
        #// to get set with the value that was originally stored in the database when the draft was created.
        #//
        if (not (php_isset(lambda : content_struct_["post_date"]))):
            post_["post_date"] = None
        # end if
        self.escape(post_)
        merged_content_struct_ = php_array_merge(post_, content_struct_)
        retval_ = self._insert_post(user_, merged_content_struct_)
        if type(retval_).__name__ == "IXR_Error":
            return retval_
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
    def wp_deletepost(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deletePost")
        post_ = get_post(post_id_, ARRAY_A)
        if php_empty(lambda : post_["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("delete_post", post_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this post.")))
        # end if
        result_ = wp_delete_post(post_id_)
        if (not result_):
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
    def wp_getpost(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_id_ = php_int(args_[3])
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// 
            #// Filters the list of post query fields used by the given XML-RPC method.
            #// 
            #// @since 3.4.0
            #// 
            #// @param array  $fields Array of post fields. Default array contains 'post', 'terms', and 'custom_fields'.
            #// @param string $method Method name.
            #//
            fields_ = apply_filters("xmlrpc_default_post_fields", Array("post", "terms", "custom_fields"), "wp.getPost")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPost")
        post_ = get_post(post_id_, ARRAY_A)
        if php_empty(lambda : post_["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        return self._prepare_post(post_, fields_)
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
    def wp_getposts(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        filter_ = args_[3] if (php_isset(lambda : args_[3])) else Array()
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields_ = apply_filters("xmlrpc_default_post_fields", Array("post", "terms", "custom_fields"), "wp.getPosts")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPosts")
        query_ = Array()
        if (php_isset(lambda : filter_["post_type"])):
            post_type_ = get_post_type_object(filter_["post_type"])
            if (not php_bool(post_type_)):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid post type.")))
            # end if
        else:
            post_type_ = get_post_type_object("post")
        # end if
        if (not current_user_can(post_type_.cap.edit_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts in this post type.")))
        # end if
        query_["post_type"] = post_type_.name
        if (php_isset(lambda : filter_["post_status"])):
            query_["post_status"] = filter_["post_status"]
        # end if
        if (php_isset(lambda : filter_["number"])):
            query_["numberposts"] = absint(filter_["number"])
        # end if
        if (php_isset(lambda : filter_["offset"])):
            query_["offset"] = absint(filter_["offset"])
        # end if
        if (php_isset(lambda : filter_["orderby"])):
            query_["orderby"] = filter_["orderby"]
            if (php_isset(lambda : filter_["order"])):
                query_["order"] = filter_["order"]
            # end if
        # end if
        if (php_isset(lambda : filter_["s"])):
            query_["s"] = filter_["s"]
        # end if
        posts_list_ = wp_get_recent_posts(query_)
        if (not posts_list_):
            return Array()
        # end if
        #// Holds all the posts data.
        struct_ = Array()
        for post_ in posts_list_:
            if (not current_user_can("edit_post", post_["ID"])):
                continue
            # end if
            struct_[-1] = self._prepare_post(post_, fields_)
        # end for
        return struct_
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
    def wp_newterm(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        content_struct_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newTerm")
        if (not taxonomy_exists(content_struct_["taxonomy"])):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy_ = get_taxonomy(content_struct_["taxonomy"])
        if (not current_user_can(taxonomy_.cap.edit_terms)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to create terms in this taxonomy.")))
        # end if
        taxonomy_ = taxonomy_
        #// Hold the data of the term.
        term_data_ = Array()
        term_data_["name"] = php_trim(content_struct_["name"])
        if php_empty(lambda : term_data_["name"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("The term name cannot be empty.")))
        # end if
        if (php_isset(lambda : content_struct_["parent"])):
            if (not taxonomy_["hierarchical"]):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("This taxonomy is not hierarchical.")))
            # end if
            parent_term_id_ = php_int(content_struct_["parent"])
            parent_term_ = get_term(parent_term_id_, taxonomy_["name"])
            if is_wp_error(parent_term_):
                return php_new_class("IXR_Error", lambda : IXR_Error(500, parent_term_.get_error_message()))
            # end if
            if (not parent_term_):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Parent term does not exist.")))
            # end if
            term_data_["parent"] = content_struct_["parent"]
        # end if
        if (php_isset(lambda : content_struct_["description"])):
            term_data_["description"] = content_struct_["description"]
        # end if
        if (php_isset(lambda : content_struct_["slug"])):
            term_data_["slug"] = content_struct_["slug"]
        # end if
        term_ = wp_insert_term(term_data_["name"], taxonomy_["name"], term_data_)
        if is_wp_error(term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term_.get_error_message()))
        # end if
        if (not term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the term could not be created.")))
        # end if
        #// Add term meta.
        if (php_isset(lambda : content_struct_["custom_fields"])):
            self.set_term_custom_fields(term_["term_id"], content_struct_["custom_fields"])
        # end if
        return php_strval(term_["term_id"])
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
    def wp_editterm(self, args_=None):
        
        
        if (not self.minimum_args(args_, 5)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        term_id_ = php_int(args_[3])
        content_struct_ = args_[4]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editTerm")
        if (not taxonomy_exists(content_struct_["taxonomy"])):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy_ = get_taxonomy(content_struct_["taxonomy"])
        taxonomy_ = taxonomy_
        #// Hold the data of the term.
        term_data_ = Array()
        term_ = get_term(term_id_, content_struct_["taxonomy"])
        if is_wp_error(term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term_.get_error_message()))
        # end if
        if (not term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid term ID.")))
        # end if
        if (not current_user_can("edit_term", term_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this term.")))
        # end if
        if (php_isset(lambda : content_struct_["name"])):
            term_data_["name"] = php_trim(content_struct_["name"])
            if php_empty(lambda : term_data_["name"]):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("The term name cannot be empty.")))
            # end if
        # end if
        if (not php_empty(lambda : content_struct_["parent"])):
            if (not taxonomy_["hierarchical"]):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Cannot set parent term, taxonomy is not hierarchical.")))
            # end if
            parent_term_id_ = php_int(content_struct_["parent"])
            parent_term_ = get_term(parent_term_id_, taxonomy_["name"])
            if is_wp_error(parent_term_):
                return php_new_class("IXR_Error", lambda : IXR_Error(500, parent_term_.get_error_message()))
            # end if
            if (not parent_term_):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Parent term does not exist.")))
            # end if
            term_data_["parent"] = content_struct_["parent"]
        # end if
        if (php_isset(lambda : content_struct_["description"])):
            term_data_["description"] = content_struct_["description"]
        # end if
        if (php_isset(lambda : content_struct_["slug"])):
            term_data_["slug"] = content_struct_["slug"]
        # end if
        term_ = wp_update_term(term_id_, taxonomy_["name"], term_data_)
        if is_wp_error(term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term_.get_error_message()))
        # end if
        if (not term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, editing the term failed.")))
        # end if
        #// Update term meta.
        if (php_isset(lambda : content_struct_["custom_fields"])):
            self.set_term_custom_fields(term_id_, content_struct_["custom_fields"])
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
    def wp_deleteterm(self, args_=None):
        
        
        if (not self.minimum_args(args_, 5)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        taxonomy_ = args_[3]
        term_id_ = php_int(args_[4])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deleteTerm")
        if (not taxonomy_exists(taxonomy_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy_ = get_taxonomy(taxonomy_)
        term_ = get_term(term_id_, taxonomy_.name)
        if is_wp_error(term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term_.get_error_message()))
        # end if
        if (not term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid term ID.")))
        # end if
        if (not current_user_can("delete_term", term_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this term.")))
        # end if
        result_ = wp_delete_term(term_id_, taxonomy_.name)
        if is_wp_error(result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term_.get_error_message()))
        # end if
        if (not result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, deleting the term failed.")))
        # end if
        return result_
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
    def wp_getterm(self, args_=None):
        
        
        if (not self.minimum_args(args_, 5)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        taxonomy_ = args_[3]
        term_id_ = php_int(args_[4])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTerm")
        if (not taxonomy_exists(taxonomy_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy_ = get_taxonomy(taxonomy_)
        term_ = get_term(term_id_, taxonomy_.name, ARRAY_A)
        if is_wp_error(term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, term_.get_error_message()))
        # end if
        if (not term_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid term ID.")))
        # end if
        if (not current_user_can("assign_term", term_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign this term.")))
        # end if
        return self._prepare_term(term_)
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
    def wp_getterms(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        taxonomy_ = args_[3]
        filter_ = args_[4] if (php_isset(lambda : args_[4])) else Array()
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTerms")
        if (not taxonomy_exists(taxonomy_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy_ = get_taxonomy(taxonomy_)
        if (not current_user_can(taxonomy_.cap.assign_terms)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign terms in this taxonomy.")))
        # end if
        query_ = Array({"taxonomy": taxonomy_.name})
        if (php_isset(lambda : filter_["number"])):
            query_["number"] = absint(filter_["number"])
        # end if
        if (php_isset(lambda : filter_["offset"])):
            query_["offset"] = absint(filter_["offset"])
        # end if
        if (php_isset(lambda : filter_["orderby"])):
            query_["orderby"] = filter_["orderby"]
            if (php_isset(lambda : filter_["order"])):
                query_["order"] = filter_["order"]
            # end if
        # end if
        if (php_isset(lambda : filter_["hide_empty"])):
            query_["hide_empty"] = filter_["hide_empty"]
        else:
            query_["get"] = "all"
        # end if
        if (php_isset(lambda : filter_["search"])):
            query_["search"] = filter_["search"]
        # end if
        terms_ = get_terms(query_)
        if is_wp_error(terms_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, terms_.get_error_message()))
        # end if
        struct_ = Array()
        for term_ in terms_:
            struct_[-1] = self._prepare_term(term_)
        # end for
        return struct_
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
    def wp_gettaxonomy(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        taxonomy_ = args_[3]
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// 
            #// Filters the taxonomy query fields used by the given XML-RPC method.
            #// 
            #// @since 3.4.0
            #// 
            #// @param array  $fields An array of taxonomy fields to retrieve.
            #// @param string $method The method name.
            #//
            fields_ = apply_filters("xmlrpc_default_taxonomy_fields", Array("labels", "cap", "object_type"), "wp.getTaxonomy")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTaxonomy")
        if (not taxonomy_exists(taxonomy_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid taxonomy.")))
        # end if
        taxonomy_ = get_taxonomy(taxonomy_)
        if (not current_user_can(taxonomy_.cap.assign_terms)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to assign terms in this taxonomy.")))
        # end if
        return self._prepare_taxonomy(taxonomy_, fields_)
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
    def wp_gettaxonomies(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        filter_ = args_[3] if (php_isset(lambda : args_[3])) else Array({"public": True})
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields_ = apply_filters("xmlrpc_default_taxonomy_fields", Array("labels", "cap", "object_type"), "wp.getTaxonomies")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getTaxonomies")
        taxonomies_ = get_taxonomies(filter_, "objects")
        #// Holds all the taxonomy data.
        struct_ = Array()
        for taxonomy_ in taxonomies_:
            #// Capability check for post types.
            if (not current_user_can(taxonomy_.cap.assign_terms)):
                continue
            # end if
            struct_[-1] = self._prepare_taxonomy(taxonomy_, fields_)
        # end for
        return struct_
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
    def wp_getuser(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_id_ = php_int(args_[3])
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// 
            #// Filters the default user query fields used by the given XML-RPC method.
            #// 
            #// @since 3.5.0
            #// 
            #// @param array  $fields User query fields for given method. Default 'all'.
            #// @param string $method The method name.
            #//
            fields_ = apply_filters("xmlrpc_default_user_fields", Array("all"), "wp.getUser")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getUser")
        if (not current_user_can("edit_user", user_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this user.")))
        # end if
        user_data_ = get_userdata(user_id_)
        if (not user_data_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid user ID.")))
        # end if
        return self._prepare_user(user_data_, fields_)
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
    def wp_getusers(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        filter_ = args_[3] if (php_isset(lambda : args_[3])) else Array()
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields_ = apply_filters("xmlrpc_default_user_fields", Array("all"), "wp.getUsers")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getUsers")
        if (not current_user_can("list_users")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to list users.")))
        # end if
        query_ = Array({"fields": "all_with_meta"})
        query_["number"] = absint(filter_["number"]) if (php_isset(lambda : filter_["number"])) else 50
        query_["offset"] = absint(filter_["offset"]) if (php_isset(lambda : filter_["offset"])) else 0
        if (php_isset(lambda : filter_["orderby"])):
            query_["orderby"] = filter_["orderby"]
            if (php_isset(lambda : filter_["order"])):
                query_["order"] = filter_["order"]
            # end if
        # end if
        if (php_isset(lambda : filter_["role"])):
            if get_role(filter_["role"]) == None:
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid role.")))
            # end if
            query_["role"] = filter_["role"]
        # end if
        if (php_isset(lambda : filter_["who"])):
            query_["who"] = filter_["who"]
        # end if
        users_ = get_users(query_)
        _users_ = Array()
        for user_data_ in users_:
            if current_user_can("edit_user", user_data_.ID):
                _users_[-1] = self._prepare_user(user_data_, fields_)
            # end if
        # end for
        return _users_
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
    def wp_getprofile(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        if (php_isset(lambda : args_[3])):
            fields_ = args_[3]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields_ = apply_filters("xmlrpc_default_user_fields", Array("all"), "wp.getProfile")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getProfile")
        if (not current_user_can("edit_user", user_.ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit your profile.")))
        # end if
        user_data_ = get_userdata(user_.ID)
        return self._prepare_user(user_data_, fields_)
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
    def wp_editprofile(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        content_struct_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editProfile")
        if (not current_user_can("edit_user", user_.ID)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit your profile.")))
        # end if
        #// Holds data of the user.
        user_data_ = Array()
        user_data_["ID"] = user_.ID
        #// Only set the user details if they were given.
        if (php_isset(lambda : content_struct_["first_name"])):
            user_data_["first_name"] = content_struct_["first_name"]
        # end if
        if (php_isset(lambda : content_struct_["last_name"])):
            user_data_["last_name"] = content_struct_["last_name"]
        # end if
        if (php_isset(lambda : content_struct_["url"])):
            user_data_["user_url"] = content_struct_["url"]
        # end if
        if (php_isset(lambda : content_struct_["display_name"])):
            user_data_["display_name"] = content_struct_["display_name"]
        # end if
        if (php_isset(lambda : content_struct_["nickname"])):
            user_data_["nickname"] = content_struct_["nickname"]
        # end if
        if (php_isset(lambda : content_struct_["nicename"])):
            user_data_["user_nicename"] = content_struct_["nicename"]
        # end if
        if (php_isset(lambda : content_struct_["bio"])):
            user_data_["description"] = content_struct_["bio"]
        # end if
        result_ = wp_update_user(user_data_)
        if is_wp_error(result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, result_.get_error_message()))
        # end if
        if (not result_):
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
    def wp_getpage(self, args_=None):
        
        
        self.escape(args_)
        page_id_ = php_int(args_[1])
        username_ = args_[2]
        password_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        page_ = get_post(page_id_)
        if (not page_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_page", page_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this page.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPage")
        #// If we found the page then format the data.
        if page_.ID and "page" == page_.post_type:
            return self._prepare_page(page_)
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
    def wp_getpages(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        num_pages_ = php_int(args_[3]) if (php_isset(lambda : args_[3])) else 10
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit pages.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPages")
        pages_ = get_posts(Array({"post_type": "page", "post_status": "any", "numberposts": num_pages_}))
        num_pages_ = php_count(pages_)
        #// If we have pages, put together their info.
        if num_pages_ >= 1:
            pages_struct_ = Array()
            for page_ in pages_:
                if current_user_can("edit_page", page_.ID):
                    pages_struct_[-1] = self._prepare_page(page_)
                # end if
            # end for
            return pages_struct_
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
    def wp_newpage(self, args_=None):
        
        
        #// Items not escaped here will be escaped in wp_newPost().
        username_ = self.escape(args_[1])
        password_ = self.escape(args_[2])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newPage")
        #// Mark this as content for a page.
        args_[3]["post_type"] = "page"
        #// Let mw_newPost() do all of the heavy lifting.
        return self.mw_newpost(args_)
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
    def wp_deletepage(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        page_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deletePage")
        #// Get the current page based on the 'page_id' and
        #// make sure it is a page and not a post.
        actual_page_ = get_post(page_id_, ARRAY_A)
        if (not actual_page_) or "page" != actual_page_["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such page.")))
        # end if
        #// Make sure the user can delete pages.
        if (not current_user_can("delete_page", page_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this page.")))
        # end if
        #// Attempt to delete the page.
        result_ = wp_delete_post(page_id_)
        if (not result_):
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
        do_action("xmlrpc_call_success_wp_deletePage", page_id_, args_)
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
    def wp_editpage(self, args_=None):
        
        
        #// Items will be escaped in mw_editPost().
        page_id_ = php_int(args_[1])
        username_ = args_[2]
        password_ = args_[3]
        content_ = args_[4]
        publish_ = args_[5]
        escaped_username_ = self.escape(username_)
        escaped_password_ = self.escape(password_)
        user_ = self.login(escaped_username_, escaped_password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editPage")
        #// Get the page data and make sure it is a page.
        actual_page_ = get_post(page_id_, ARRAY_A)
        if (not actual_page_) or "page" != actual_page_["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such page.")))
        # end if
        #// Make sure the user is allowed to edit pages.
        if (not current_user_can("edit_page", page_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this page.")))
        # end if
        #// Mark this as content for a page.
        content_["post_type"] = "page"
        #// Arrange args in the way mw_editPost() understands.
        args_ = Array(page_id_, username_, password_, content_, publish_)
        #// Let mw_editPost() do all of the heavy lifting.
        return self.mw_editpost(args_)
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
    def wp_getpagelist(self, args_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit pages.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPageList")
        #// Get list of page IDs and titles.
        page_list_ = wpdb_.get_results(str("""\n            SELECT ID page_id,\n                post_title page_title,\n                post_parent page_parent_id,\n               post_date_gmt,\n                post_date,\n                post_status\n           FROM """) + str(wpdb_.posts) + str("""\n            WHERE post_type = 'page'\n          ORDER BY ID\n       """))
        #// The date needs to be formatted properly.
        num_pages_ = php_count(page_list_)
        i_ = 0
        while i_ < num_pages_:
            
            page_list_[i_].dateCreated = self._convert_date(page_list_[i_].post_date)
            page_list_[i_].date_created_gmt = self._convert_date_gmt(page_list_[i_].post_date_gmt, page_list_[i_].post_date)
            page_list_[i_].post_date_gmt = None
            page_list_[i_].post_date = None
            page_list_[i_].post_status = None
            i_ += 1
        # end while
        return page_list_
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
    def wp_getauthors(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getAuthors")
        authors_ = Array()
        for user_ in get_users(Array({"fields": Array("ID", "user_login", "display_name")})):
            authors_[-1] = Array({"user_id": user_.ID, "user_login": user_.user_login, "display_name": user_.display_name})
        # end for
        return authors_
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
    def wp_gettags(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view tags.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getKeywords")
        tags_ = Array()
        all_tags_ = get_tags()
        if all_tags_:
            for tag_ in all_tags_:
                struct_ = Array()
                struct_["tag_id"] = tag_.term_id
                struct_["name"] = tag_.name
                struct_["count"] = tag_.count
                struct_["slug"] = tag_.slug
                struct_["html_url"] = esc_html(get_tag_link(tag_.term_id))
                struct_["rss_url"] = esc_html(get_tag_feed_link(tag_.term_id))
                tags_[-1] = struct_
            # end for
        # end if
        return tags_
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
    def wp_newcategory(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        category_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
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
        if php_empty(lambda : category_["slug"]):
            category_["slug"] = ""
        # end if
        #// If no parent_id was provided, make it empty
        #// so that it will be a top-level page (no parent).
        if (not (php_isset(lambda : category_["parent_id"]))):
            category_["parent_id"] = ""
        # end if
        #// If no description was provided, make it empty.
        if php_empty(lambda : category_["description"]):
            category_["description"] = ""
        # end if
        new_category_ = Array({"cat_name": category_["name"], "category_nicename": category_["slug"], "category_parent": category_["parent_id"], "category_description": category_["description"]})
        cat_id_ = wp_insert_category(new_category_, True)
        if is_wp_error(cat_id_):
            if "term_exists" == cat_id_.get_error_code():
                return php_int(cat_id_.get_error_data())
            else:
                return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the category could not be created.")))
            # end if
        elif (not cat_id_):
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
        do_action("xmlrpc_call_success_wp_newCategory", cat_id_, args_)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return cat_id_
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
    def wp_deletecategory(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        category_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deleteCategory")
        if (not current_user_can("delete_term", category_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this category.")))
        # end if
        status_ = wp_delete_term(category_id_, "category")
        if True == status_:
            #// 
            #// Fires after a category has been successfully deleted via XML-RPC.
            #// 
            #// @since 3.4.0
            #// 
            #// @param int   $category_id ID of the deleted category.
            #// @param array $args        An array of arguments to delete the category.
            #//
            do_action("xmlrpc_call_success_wp_deleteCategory", category_id_, args_)
            pass
        # end if
        return status_
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
    def wp_suggestcategories(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        category_ = args_[3]
        max_results_ = php_int(args_[4])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view categories.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.suggestCategories")
        category_suggestions_ = Array()
        args_ = Array({"get": "all", "number": max_results_, "name__like": category_})
        for cat_ in get_categories(args_):
            category_suggestions_[-1] = Array({"category_id": cat_.term_id, "category_name": cat_.name})
        # end for
        return category_suggestions_
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
    def wp_getcomment(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        comment_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getComment")
        comment_ = get_comment(comment_id_)
        if (not comment_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid comment ID.")))
        # end if
        if (not current_user_can("edit_comment", comment_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to moderate or edit this comment.")))
        # end if
        return self._prepare_comment(comment_)
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
    def wp_getcomments(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        struct_ = args_[3] if (php_isset(lambda : args_[3])) else Array()
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getComments")
        if (php_isset(lambda : struct_["status"])):
            status_ = struct_["status"]
        else:
            status_ = ""
        # end if
        if (not current_user_can("moderate_comments")) and "approve" != status_:
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid comment status.")))
        # end if
        post_id_ = ""
        if (php_isset(lambda : struct_["post_id"])):
            post_id_ = absint(struct_["post_id"])
        # end if
        post_type_ = ""
        if (php_isset(lambda : struct_["post_type"])):
            post_type_object_ = get_post_type_object(struct_["post_type"])
            if (not post_type_object_) or (not post_type_supports(post_type_object_.name, "comments")):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post type.")))
            # end if
            post_type_ = struct_["post_type"]
        # end if
        offset_ = 0
        if (php_isset(lambda : struct_["offset"])):
            offset_ = absint(struct_["offset"])
        # end if
        number_ = 10
        if (php_isset(lambda : struct_["number"])):
            number_ = absint(struct_["number"])
        # end if
        comments_ = get_comments(Array({"status": status_, "post_id": post_id_, "offset": offset_, "number": number_, "post_type": post_type_}))
        comments_struct_ = Array()
        if php_is_array(comments_):
            for comment_ in comments_:
                comments_struct_[-1] = self._prepare_comment(comment_)
            # end for
        # end if
        return comments_struct_
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
    def wp_deletecomment(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        comment_ID_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not get_comment(comment_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid comment ID.")))
        # end if
        if (not current_user_can("edit_comment", comment_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to delete this comment.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.deleteComment")
        status_ = wp_delete_comment(comment_ID_)
        if status_:
            #// 
            #// Fires after a comment has been successfully deleted via XML-RPC.
            #// 
            #// @since 3.4.0
            #// 
            #// @param int   $comment_ID ID of the deleted comment.
            #// @param array $args       An array of arguments to delete the comment.
            #//
            do_action("xmlrpc_call_success_wp_deleteComment", comment_ID_, args_)
            pass
        # end if
        return status_
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
    def wp_editcomment(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        comment_ID_ = php_int(args_[3])
        content_struct_ = args_[4]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not get_comment(comment_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid comment ID.")))
        # end if
        if (not current_user_can("edit_comment", comment_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to moderate or edit this comment.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.editComment")
        comment_ = Array({"comment_ID": comment_ID_})
        if (php_isset(lambda : content_struct_["status"])):
            statuses_ = get_comment_statuses()
            statuses_ = php_array_keys(statuses_)
            if (not php_in_array(content_struct_["status"], statuses_)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid comment status.")))
            # end if
            comment_["comment_approved"] = content_struct_["status"]
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : content_struct_["date_created_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated_ = php_rtrim(content_struct_["date_created_gmt"].getiso(), "Z") + "Z"
            comment_["comment_date"] = get_date_from_gmt(dateCreated_)
            comment_["comment_date_gmt"] = iso8601_to_datetime(dateCreated_, "gmt")
        # end if
        if (php_isset(lambda : content_struct_["content"])):
            comment_["comment_content"] = content_struct_["content"]
        # end if
        if (php_isset(lambda : content_struct_["author"])):
            comment_["comment_author"] = content_struct_["author"]
        # end if
        if (php_isset(lambda : content_struct_["author_url"])):
            comment_["comment_author_url"] = content_struct_["author_url"]
        # end if
        if (php_isset(lambda : content_struct_["author_email"])):
            comment_["comment_author_email"] = content_struct_["author_email"]
        # end if
        result_ = wp_update_comment(comment_)
        if is_wp_error(result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, result_.get_error_message()))
        # end if
        if (not result_):
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
        do_action("xmlrpc_call_success_wp_editComment", comment_ID_, args_)
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
    def wp_newcomment(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_ = args_[3]
        content_struct_ = args_[4]
        #// 
        #// Filters whether to allow anonymous comments over XML-RPC.
        #// 
        #// @since 2.7.0
        #// 
        #// @param bool $allow Whether to allow anonymous commenting via XML-RPC.
        #// Default false.
        #//
        allow_anon_ = apply_filters("xmlrpc_allow_anonymous_comments", False)
        user_ = self.login(username_, password_)
        if (not user_):
            logged_in_ = False
            if allow_anon_ and get_option("comment_registration"):
                return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you must be logged in to comment.")))
            elif (not allow_anon_):
                return self.error
            # end if
        else:
            logged_in_ = True
        # end if
        if php_is_numeric(post_):
            post_id_ = absint(post_)
        else:
            post_id_ = url_to_postid(post_)
        # end if
        if (not post_id_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not get_post(post_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not comments_open(post_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, comments are closed for this item.")))
        # end if
        if php_empty(lambda : content_struct_["content"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Comment is required.")))
        # end if
        comment_ = Array({"comment_post_ID": post_id_, "comment_content": content_struct_["content"]})
        if logged_in_:
            display_name_ = user_.display_name
            user_email_ = user_.user_email
            user_url_ = user_.user_url
            comment_["comment_author"] = self.escape(display_name_)
            comment_["comment_author_email"] = self.escape(user_email_)
            comment_["comment_author_url"] = self.escape(user_url_)
            comment_["user_ID"] = user_.ID
        else:
            comment_["comment_author"] = ""
            if (php_isset(lambda : content_struct_["author"])):
                comment_["comment_author"] = content_struct_["author"]
            # end if
            comment_["comment_author_email"] = ""
            if (php_isset(lambda : content_struct_["author_email"])):
                comment_["comment_author_email"] = content_struct_["author_email"]
            # end if
            comment_["comment_author_url"] = ""
            if (php_isset(lambda : content_struct_["author_url"])):
                comment_["comment_author_url"] = content_struct_["author_url"]
            # end if
            comment_["user_ID"] = 0
            if get_option("require_name_email"):
                if 6 > php_strlen(comment_["comment_author_email"]) or "" == comment_["comment_author"]:
                    return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Comment author name and email are required.")))
                elif (not is_email(comment_["comment_author_email"])):
                    return php_new_class("IXR_Error", lambda : IXR_Error(403, __("A valid email address is required.")))
                # end if
            # end if
        # end if
        comment_["comment_parent"] = absint(content_struct_["comment_parent"]) if (php_isset(lambda : content_struct_["comment_parent"])) else 0
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.newComment")
        comment_ID_ = wp_new_comment(comment_, True)
        if is_wp_error(comment_ID_):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, comment_ID_.get_error_message()))
        # end if
        if (not comment_ID_):
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
        do_action("xmlrpc_call_success_wp_newComment", comment_ID_, args_)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return comment_ID_
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
    def wp_getcommentstatuslist(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
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
    def wp_getcommentcount(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        post_ = get_post(post_id_, ARRAY_A)
        if php_empty(lambda : post_["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details of this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getCommentCount")
        count_ = wp_count_comments(post_id_)
        return Array({"approved": count_.approved, "awaiting_moderation": count_.moderated, "spam": count_.spam, "total_comments": count_.total_comments})
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
    def wp_getpoststatuslist(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
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
    def wp_getpagestatuslist(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
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
    def wp_getpagetemplates(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_pages")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        templates_ = get_page_templates()
        templates_["Default"] = "default"
        return templates_
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
    def wp_getoptions(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        options_ = args_[3] if (php_isset(lambda : args_[3])) else Array()
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// If no specific options where asked for, return all of them.
        if php_count(options_) == 0:
            options_ = php_array_keys(self.blog_options)
        # end if
        return self._getoptions(options_)
    # end def wp_getoptions
    #// 
    #// Retrieve blog options value from list.
    #// 
    #// @since 2.6.0
    #// 
    #// @param array $options Options to retrieve.
    #// @return array
    #//
    def _getoptions(self, options_=None):
        
        
        data_ = Array()
        can_manage_ = current_user_can("manage_options")
        for option_ in options_:
            if php_array_key_exists(option_, self.blog_options):
                data_[option_] = self.blog_options[option_]
                #// Is the value static or dynamic?
                if (php_isset(lambda : data_[option_]["option"])):
                    data_[option_]["value"] = get_option(data_[option_]["option"])
                    data_[option_]["option"] = None
                # end if
                if (not can_manage_):
                    data_[option_]["readonly"] = True
                # end if
            # end if
        # end for
        return data_
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
    def wp_setoptions(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        options_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("manage_options")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to update options.")))
        # end if
        option_names_ = Array()
        for o_name_,o_value_ in options_:
            option_names_[-1] = o_name_
            if (not php_array_key_exists(o_name_, self.blog_options)):
                continue
            # end if
            if True == self.blog_options[o_name_]["readonly"]:
                continue
            # end if
            update_option(self.blog_options[o_name_]["option"], wp_unslash(o_value_))
        # end for
        #// Now return the updated values.
        return self._getoptions(option_names_)
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
    def wp_getmediaitem(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        attachment_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("upload_files")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to upload files.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getMediaItem")
        attachment_ = get_post(attachment_id_)
        if (not attachment_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
        # end if
        return self._prepare_media_item(attachment_)
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
    def wp_getmedialibrary(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        struct_ = args_[3] if (php_isset(lambda : args_[3])) else Array()
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("upload_files")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to upload files.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getMediaLibrary")
        parent_id_ = absint(struct_["parent_id"]) if (php_isset(lambda : struct_["parent_id"])) else ""
        mime_type_ = struct_["mime_type"] if (php_isset(lambda : struct_["mime_type"])) else ""
        offset_ = absint(struct_["offset"]) if (php_isset(lambda : struct_["offset"])) else 0
        number_ = absint(struct_["number"]) if (php_isset(lambda : struct_["number"])) else -1
        attachments_ = get_posts(Array({"post_type": "attachment", "post_parent": parent_id_, "offset": offset_, "numberposts": number_, "post_mime_type": mime_type_}))
        attachments_struct_ = Array()
        for attachment_ in attachments_:
            attachments_struct_[-1] = self._prepare_media_item(attachment_)
        # end for
        return attachments_struct_
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
    def wp_getpostformats(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Sorry, you are not allowed to access details about this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostFormats")
        formats_ = get_post_format_strings()
        #// Find out if they want a list of currently supports formats.
        if (php_isset(lambda : args_[3])) and php_is_array(args_[3]):
            if args_[3]["show-supported"]:
                if current_theme_supports("post-formats"):
                    supported_ = get_theme_support("post-formats")
                    data_ = Array()
                    data_["all"] = formats_
                    data_["supported"] = supported_[0]
                    formats_ = data_
                # end if
            # end if
        # end if
        return formats_
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
    def wp_getposttype(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_type_name_ = args_[3]
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// 
            #// Filters the default query fields used by the given XML-RPC method.
            #// 
            #// @since 3.4.0
            #// 
            #// @param array  $fields An array of post type query fields for the given method.
            #// @param string $method The method name.
            #//
            fields_ = apply_filters("xmlrpc_default_posttype_fields", Array("labels", "cap", "taxonomies"), "wp.getPostType")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostType")
        if (not post_type_exists(post_type_name_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(403, __("Invalid post type.")))
        # end if
        post_type_ = get_post_type_object(post_type_name_)
        if (not current_user_can(post_type_.cap.edit_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts in this post type.")))
        # end if
        return self._prepare_post_type(post_type_, fields_)
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
    def wp_getposttypes(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        filter_ = args_[3] if (php_isset(lambda : args_[3])) else Array({"public": True})
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
            fields_ = apply_filters("xmlrpc_default_posttype_fields", Array("labels", "cap", "taxonomies"), "wp.getPostTypes")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getPostTypes")
        post_types_ = get_post_types(filter_, "objects")
        struct_ = Array()
        for post_type_ in post_types_:
            if (not current_user_can(post_type_.cap.edit_posts)):
                continue
            # end if
            struct_[post_type_.name] = self._prepare_post_type(post_type_, fields_)
        # end for
        return struct_
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
    def wp_getrevisions(self, args_=None):
        
        
        if (not self.minimum_args(args_, 4)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        post_id_ = php_int(args_[3])
        if (php_isset(lambda : args_[4])):
            fields_ = args_[4]
        else:
            #// 
            #// Filters the default revision query fields used by the given XML-RPC method.
            #// 
            #// @since 3.5.0
            #// 
            #// @param array  $field  An array of revision query fields.
            #// @param string $method The method name.
            #//
            fields_ = apply_filters("xmlrpc_default_revision_fields", Array("post_date", "post_date_gmt"), "wp.getRevisions")
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.getRevisions")
        post_ = get_post(post_id_)
        if (not post_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_id_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// Check if revisions are enabled.
        if (not wp_revisions_enabled(post_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, revisions are disabled.")))
        # end if
        revisions_ = wp_get_post_revisions(post_id_)
        if (not revisions_):
            return Array()
        # end if
        struct_ = Array()
        for revision_ in revisions_:
            if (not current_user_can("read_post", revision_.ID)):
                continue
            # end if
            #// Skip autosaves.
            if wp_is_post_autosave(revision_):
                continue
            # end if
            struct_[-1] = self._prepare_post(get_object_vars(revision_), fields_)
        # end for
        return struct_
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
    def wp_restorerevision(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        revision_id_ = php_int(args_[3])
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "wp.restoreRevision")
        revision_ = wp_get_post_revision(revision_id_)
        if (not revision_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if wp_is_post_autosave(revision_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        post_ = get_post(revision_.post_parent)
        if (not post_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", revision_.post_parent)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// Check if revisions are disabled.
        if (not wp_revisions_enabled(post_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, revisions are disabled.")))
        # end if
        post_ = wp_restore_post_revision(revision_id_)
        return php_bool(post_)
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
    def blogger_getusersblogs(self, args_=None):
        
        
        if (not self.minimum_args(args_, 3)):
            return self.error
        # end if
        if is_multisite():
            return self._multisite_getusersblogs(args_)
        # end if
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getUsersBlogs")
        is_admin_ = current_user_can("manage_options")
        struct_ = Array({"isAdmin": is_admin_, "url": get_option("home") + "/", "blogid": "1", "blogName": get_option("blogname"), "xmlrpc": site_url("xmlrpc.php", "rpc")})
        return Array(struct_)
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
    def _multisite_getusersblogs(self, args_=None):
        
        
        current_blog_ = get_site()
        domain_ = current_blog_.domain
        path_ = current_blog_.path + "xmlrpc.php"
        rpc_ = php_new_class("IXR_Client", lambda : IXR_Client(set_url_scheme(str("http://") + str(domain_) + str(path_))))
        rpc_.query("wp.getUsersBlogs", args_[1], args_[2])
        blogs_ = rpc_.getresponse()
        if (php_isset(lambda : blogs_["faultCode"])):
            return php_new_class("IXR_Error", lambda : IXR_Error(blogs_["faultCode"], blogs_["faultString"]))
        # end if
        if PHP_SERVER["HTTP_HOST"] == domain_ and PHP_SERVER["REQUEST_URI"] == path_:
            return blogs_
        else:
            for blog_ in blogs_:
                if php_strpos(blog_["url"], PHP_SERVER["HTTP_HOST"]):
                    return Array(blog_)
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
    def blogger_getuserinfo(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to access user data on this site.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getUserInfo")
        struct_ = Array({"nickname": user_.nickname, "userid": user_.ID, "url": user_.user_url, "lastname": user_.last_name, "firstname": user_.first_name})
        return struct_
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
    def blogger_getpost(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[1])
        username_ = args_[2]
        password_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        post_data_ = get_post(post_ID_, ARRAY_A)
        if (not post_data_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getPost")
        categories_ = php_implode(",", wp_get_post_categories(post_ID_))
        content_ = "<title>" + wp_unslash(post_data_["post_title"]) + "</title>"
        content_ += "<category>" + categories_ + "</category>"
        content_ += wp_unslash(post_data_["post_content"])
        struct_ = Array({"userid": post_data_["post_author"], "dateCreated": self._convert_date(post_data_["post_date"]), "content": content_, "postid": php_str(post_data_["ID"])})
        return struct_
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
    def blogger_getrecentposts(self, args_=None):
        
        
        self.escape(args_)
        #// $args[0] = appkey - ignored.
        username_ = args_[2]
        password_ = args_[3]
        if (php_isset(lambda : args_[4])):
            query_ = Array({"numberposts": absint(args_[4])})
        else:
            query_ = Array()
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.getRecentPosts")
        posts_list_ = wp_get_recent_posts(query_)
        if (not posts_list_):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(500, __("Either there are no posts, or something went wrong.")))
            return self.error
        # end if
        recent_posts_ = Array()
        for entry_ in posts_list_:
            if (not current_user_can("edit_post", entry_["ID"])):
                continue
            # end if
            post_date_ = self._convert_date(entry_["post_date"])
            categories_ = php_implode(",", wp_get_post_categories(entry_["ID"]))
            content_ = "<title>" + wp_unslash(entry_["post_title"]) + "</title>"
            content_ += "<category>" + categories_ + "</category>"
            content_ += wp_unslash(entry_["post_content"])
            recent_posts_[-1] = Array({"userid": entry_["post_author"], "dateCreated": post_date_, "content": content_, "postid": php_str(entry_["ID"])})
        # end for
        return recent_posts_
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
    def blogger_gettemplate(self, args_=None):
        
        
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
    def blogger_settemplate(self, args_=None):
        
        
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
    def blogger_newpost(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[2]
        password_ = args_[3]
        content_ = args_[4]
        publish_ = args_[5]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.newPost")
        cap_ = "publish_posts" if publish_ else "edit_posts"
        if (not current_user_can(get_post_type_object("post").cap.create_posts)) or (not current_user_can(cap_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to post on this site.")))
        # end if
        post_status_ = "publish" if publish_ else "draft"
        post_author_ = user_.ID
        post_title_ = xmlrpc_getposttitle(content_)
        post_category_ = xmlrpc_getpostcategory(content_)
        post_content_ = xmlrpc_removepostdata(content_)
        post_date_ = current_time("mysql")
        post_date_gmt_ = current_time("mysql", 1)
        post_data_ = php_compact("post_author", "post_date", "post_date_gmt", "post_content", "post_title", "post_category", "post_status")
        post_ID_ = wp_insert_post(post_data_)
        if is_wp_error(post_ID_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, post_ID_.get_error_message()))
        # end if
        if (not post_ID_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be created.")))
        # end if
        self.attach_uploads(post_ID_, post_content_)
        #// 
        #// Fires after a new post has been successfully created via the XML-RPC Blogger API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the new post.
        #// @param array $args    An array of new post arguments.
        #//
        do_action("xmlrpc_call_success_blogger_newPost", post_ID_, args_)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return post_ID_
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
    def blogger_editpost(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[1])
        username_ = args_[2]
        password_ = args_[3]
        content_ = args_[4]
        publish_ = args_[5]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.editPost")
        actual_post_ = get_post(post_ID_, ARRAY_A)
        if (not actual_post_) or "post" != actual_post_["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
        self.escape(actual_post_)
        if (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        if "publish" == actual_post_["post_status"] and (not current_user_can("publish_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this post.")))
        # end if
        postdata_ = Array()
        postdata_["ID"] = actual_post_["ID"]
        postdata_["post_content"] = xmlrpc_removepostdata(content_)
        postdata_["post_title"] = xmlrpc_getposttitle(content_)
        postdata_["post_category"] = xmlrpc_getpostcategory(content_)
        postdata_["post_status"] = actual_post_["post_status"]
        postdata_["post_excerpt"] = actual_post_["post_excerpt"]
        postdata_["post_status"] = "publish" if publish_ else "draft"
        result_ = wp_update_post(postdata_)
        if (not result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be updated.")))
        # end if
        self.attach_uploads(actual_post_["ID"], postdata_["post_content"])
        #// 
        #// Fires after a post has been successfully updated via the XML-RPC Blogger API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the updated post.
        #// @param array $args    An array of arguments for the post to edit.
        #//
        do_action("xmlrpc_call_success_blogger_editPost", post_ID_, args_)
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
    def blogger_deletepost(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[1])
        username_ = args_[2]
        password_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "blogger.deletePost")
        actual_post_ = get_post(post_ID_, ARRAY_A)
        if (not actual_post_) or "post" != actual_post_["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
        if (not current_user_can("delete_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to delete this post.")))
        # end if
        result_ = wp_delete_post(post_ID_)
        if (not result_):
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
        do_action("xmlrpc_call_success_blogger_deletePost", post_ID_, args_)
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
    def mw_newpost(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        content_struct_ = args_[3]
        publish_ = args_[4] if (php_isset(lambda : args_[4])) else 0
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.newPost")
        page_template_ = ""
        if (not php_empty(lambda : content_struct_["post_type"])):
            if "page" == content_struct_["post_type"]:
                if publish_:
                    cap_ = "publish_pages"
                elif (php_isset(lambda : content_struct_["page_status"])) and "publish" == content_struct_["page_status"]:
                    cap_ = "publish_pages"
                else:
                    cap_ = "edit_pages"
                # end if
                error_message_ = __("Sorry, you are not allowed to publish pages on this site.")
                post_type_ = "page"
                if (not php_empty(lambda : content_struct_["wp_page_template"])):
                    page_template_ = content_struct_["wp_page_template"]
                # end if
            elif "post" == content_struct_["post_type"]:
                if publish_:
                    cap_ = "publish_posts"
                elif (php_isset(lambda : content_struct_["post_status"])) and "publish" == content_struct_["post_status"]:
                    cap_ = "publish_posts"
                else:
                    cap_ = "edit_posts"
                # end if
                error_message_ = __("Sorry, you are not allowed to publish posts on this site.")
                post_type_ = "post"
            else:
                #// No other 'post_type' values are allowed here.
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post type.")))
            # end if
        else:
            if publish_:
                cap_ = "publish_posts"
            elif (php_isset(lambda : content_struct_["post_status"])) and "publish" == content_struct_["post_status"]:
                cap_ = "publish_posts"
            else:
                cap_ = "edit_posts"
            # end if
            error_message_ = __("Sorry, you are not allowed to publish posts on this site.")
            post_type_ = "post"
        # end if
        if (not current_user_can(get_post_type_object(post_type_).cap.create_posts)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish posts on this site.")))
        # end if
        if (not current_user_can(cap_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, error_message_))
        # end if
        #// Check for a valid post format if one was given.
        if (php_isset(lambda : content_struct_["wp_post_format"])):
            content_struct_["wp_post_format"] = sanitize_key(content_struct_["wp_post_format"])
            if (not php_array_key_exists(content_struct_["wp_post_format"], get_post_format_strings())):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post format.")))
            # end if
        # end if
        #// Let WordPress generate the 'post_name' (slug) unless
        #// one has been provided.
        post_name_ = ""
        if (php_isset(lambda : content_struct_["wp_slug"])):
            post_name_ = content_struct_["wp_slug"]
        # end if
        #// Only use a password if one was given.
        if (php_isset(lambda : content_struct_["wp_password"])):
            post_password_ = content_struct_["wp_password"]
        else:
            post_password_ = ""
        # end if
        #// Only set a post parent if one was given.
        if (php_isset(lambda : content_struct_["wp_page_parent_id"])):
            post_parent_ = content_struct_["wp_page_parent_id"]
        else:
            post_parent_ = 0
        # end if
        #// Only set the 'menu_order' if it was given.
        if (php_isset(lambda : content_struct_["wp_page_order"])):
            menu_order_ = content_struct_["wp_page_order"]
        else:
            menu_order_ = 0
        # end if
        post_author_ = user_.ID
        #// If an author id was provided then use it instead.
        if (php_isset(lambda : content_struct_["wp_author_id"])) and user_.ID != content_struct_["wp_author_id"]:
            for case in Switch(post_type_):
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
            author_ = get_userdata(content_struct_["wp_author_id"])
            if (not author_):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid author ID.")))
            # end if
            post_author_ = content_struct_["wp_author_id"]
        # end if
        post_title_ = content_struct_["title"] if (php_isset(lambda : content_struct_["title"])) else None
        post_content_ = content_struct_["description"] if (php_isset(lambda : content_struct_["description"])) else None
        post_status_ = "publish" if publish_ else "draft"
        if (php_isset(lambda : content_struct_[str(post_type_) + str("_status")])):
            for case in Switch(content_struct_[str(post_type_) + str("_status")]):
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
                    post_status_ = content_struct_[str(post_type_) + str("_status")]
                    break
                # end if
                if case():
                    post_status_ = "publish" if publish_ else "draft"
                    break
                # end if
            # end for
        # end if
        post_excerpt_ = content_struct_["mt_excerpt"] if (php_isset(lambda : content_struct_["mt_excerpt"])) else None
        post_more_ = content_struct_["mt_text_more"] if (php_isset(lambda : content_struct_["mt_text_more"])) else None
        tags_input_ = content_struct_["mt_keywords"] if (php_isset(lambda : content_struct_["mt_keywords"])) else None
        if (php_isset(lambda : content_struct_["mt_allow_comments"])):
            if (not php_is_numeric(content_struct_["mt_allow_comments"])):
                for case in Switch(content_struct_["mt_allow_comments"]):
                    if case("closed"):
                        comment_status_ = "closed"
                        break
                    # end if
                    if case("open"):
                        comment_status_ = "open"
                        break
                    # end if
                    if case():
                        comment_status_ = get_default_comment_status(post_type_)
                        break
                    # end if
                # end for
            else:
                for case in Switch(php_int(content_struct_["mt_allow_comments"])):
                    if case(0):
                        pass
                    # end if
                    if case(2):
                        comment_status_ = "closed"
                        break
                    # end if
                    if case(1):
                        comment_status_ = "open"
                        break
                    # end if
                    if case():
                        comment_status_ = get_default_comment_status(post_type_)
                        break
                    # end if
                # end for
            # end if
        else:
            comment_status_ = get_default_comment_status(post_type_)
        # end if
        if (php_isset(lambda : content_struct_["mt_allow_pings"])):
            if (not php_is_numeric(content_struct_["mt_allow_pings"])):
                for case in Switch(content_struct_["mt_allow_pings"]):
                    if case("closed"):
                        ping_status_ = "closed"
                        break
                    # end if
                    if case("open"):
                        ping_status_ = "open"
                        break
                    # end if
                    if case():
                        ping_status_ = get_default_comment_status(post_type_, "pingback")
                        break
                    # end if
                # end for
            else:
                for case in Switch(php_int(content_struct_["mt_allow_pings"])):
                    if case(0):
                        ping_status_ = "closed"
                        break
                    # end if
                    if case(1):
                        ping_status_ = "open"
                        break
                    # end if
                    if case():
                        ping_status_ = get_default_comment_status(post_type_, "pingback")
                        break
                    # end if
                # end for
            # end if
        else:
            ping_status_ = get_default_comment_status(post_type_, "pingback")
        # end if
        if post_more_:
            post_content_ = post_content_ + "<!--more-->" + post_more_
        # end if
        to_ping_ = None
        if (php_isset(lambda : content_struct_["mt_tb_ping_urls"])):
            to_ping_ = content_struct_["mt_tb_ping_urls"]
            if php_is_array(to_ping_):
                to_ping_ = php_implode(" ", to_ping_)
            # end if
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : content_struct_["date_created_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated_ = php_rtrim(content_struct_["date_created_gmt"].getiso(), "Z") + "Z"
        elif (not php_empty(lambda : content_struct_["dateCreated"])):
            dateCreated_ = content_struct_["dateCreated"].getiso()
        # end if
        if (not php_empty(lambda : dateCreated_)):
            post_date_ = iso8601_to_datetime(dateCreated_)
            post_date_gmt_ = iso8601_to_datetime(dateCreated_, "gmt")
        else:
            post_date_ = ""
            post_date_gmt_ = ""
        # end if
        post_category_ = Array()
        if (php_isset(lambda : content_struct_["categories"])):
            catnames_ = content_struct_["categories"]
            if php_is_array(catnames_):
                for cat_ in catnames_:
                    post_category_[-1] = get_cat_ID(cat_)
                # end for
            # end if
        # end if
        postdata_ = php_compact("post_author", "post_date", "post_date_gmt", "post_content", "post_title", "post_category", "post_status", "post_excerpt", "comment_status", "ping_status", "to_ping", "post_type", "post_name", "post_password", "post_parent", "menu_order", "tags_input", "page_template")
        post_ID_ = get_default_post_to_edit(post_type_, True).ID
        postdata_["ID"] = post_ID_
        #// Only posts can be sticky.
        if "post" == post_type_ and (php_isset(lambda : content_struct_["sticky"])):
            data_ = postdata_
            data_["sticky"] = content_struct_["sticky"]
            error_ = self._toggle_sticky(data_)
            if error_:
                return error_
            # end if
        # end if
        if (php_isset(lambda : content_struct_["custom_fields"])):
            self.set_custom_fields(post_ID_, content_struct_["custom_fields"])
        # end if
        if (php_isset(lambda : content_struct_["wp_post_thumbnail"])):
            if set_post_thumbnail(post_ID_, content_struct_["wp_post_thumbnail"]) == False:
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
            # end if
            content_struct_["wp_post_thumbnail"] = None
        # end if
        #// Handle enclosures.
        thisEnclosure_ = content_struct_["enclosure"] if (php_isset(lambda : content_struct_["enclosure"])) else None
        self.add_enclosure_if_new(post_ID_, thisEnclosure_)
        self.attach_uploads(post_ID_, post_content_)
        #// Handle post formats if assigned, value is validated earlier
        #// in this function.
        if (php_isset(lambda : content_struct_["wp_post_format"])):
            set_post_format(post_ID_, content_struct_["wp_post_format"])
        # end if
        post_ID_ = wp_insert_post(postdata_, True)
        if is_wp_error(post_ID_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, post_ID_.get_error_message()))
        # end if
        if (not post_ID_):
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
        do_action("xmlrpc_call_success_mw_newPost", post_ID_, args_)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        return php_strval(post_ID_)
    # end def mw_newpost
    #// 
    #// Adds an enclosure to a post if it's new.
    #// 
    #// @since 2.8.0
    #// 
    #// @param integer $post_ID   Post ID.
    #// @param array   $enclosure Enclosure data.
    #//
    def add_enclosure_if_new(self, post_ID_=None, enclosure_=None):
        
        
        if php_is_array(enclosure_) and (php_isset(lambda : enclosure_["url"])) and (php_isset(lambda : enclosure_["length"])) and (php_isset(lambda : enclosure_["type"])):
            encstring_ = enclosure_["url"] + "\n" + enclosure_["length"] + "\n" + enclosure_["type"] + "\n"
            found_ = False
            enclosures_ = get_post_meta(post_ID_, "enclosure")
            if enclosures_:
                for enc_ in enclosures_:
                    #// This method used to omit the trailing new line. #23219
                    if php_rtrim(enc_, "\n") == php_rtrim(encstring_, "\n"):
                        found_ = True
                        break
                    # end if
                # end for
            # end if
            if (not found_):
                add_post_meta(post_ID_, "enclosure", encstring_)
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
    def attach_uploads(self, post_ID_=None, post_content_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// Find any unattached files.
        attachments_ = wpdb_.get_results(str("SELECT ID, guid FROM ") + str(wpdb_.posts) + str(" WHERE post_parent = '0' AND post_type = 'attachment'"))
        if php_is_array(attachments_):
            for file_ in attachments_:
                if (not php_empty(lambda : file_.guid)) and php_strpos(post_content_, file_.guid) != False:
                    wpdb_.update(wpdb_.posts, Array({"post_parent": post_ID_}), Array({"ID": file_.ID}))
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
    def mw_editpost(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[0])
        username_ = args_[1]
        password_ = args_[2]
        content_struct_ = args_[3]
        publish_ = args_[4] if (php_isset(lambda : args_[4])) else 0
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.editPost")
        postdata_ = get_post(post_ID_, ARRAY_A)
        #// 
        #// If there is no post data for the give post id, stop now and return an error.
        #// Otherwise a new post will be created (which was the old behavior).
        #//
        if (not postdata_) or php_empty(lambda : postdata_["ID"]):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// Use wp.editPost to edit post types other than post and page.
        if (not php_in_array(postdata_["post_type"], Array("post", "page"))):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Invalid post type.")))
        # end if
        #// Thwart attempt to change the post type.
        if (not php_empty(lambda : content_struct_["post_type"])) and content_struct_["post_type"] != postdata_["post_type"]:
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("The post type may not be changed.")))
        # end if
        #// Check for a valid post format if one was given.
        if (php_isset(lambda : content_struct_["wp_post_format"])):
            content_struct_["wp_post_format"] = sanitize_key(content_struct_["wp_post_format"])
            if (not php_array_key_exists(content_struct_["wp_post_format"], get_post_format_strings())):
                return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post format.")))
            # end if
        # end if
        self.escape(postdata_)
        ID_ = postdata_["ID"]
        post_content_ = postdata_["post_content"]
        post_title_ = postdata_["post_title"]
        post_excerpt_ = postdata_["post_excerpt"]
        post_password_ = postdata_["post_password"]
        post_parent_ = postdata_["post_parent"]
        post_type_ = postdata_["post_type"]
        menu_order_ = postdata_["menu_order"]
        ping_status_ = postdata_["ping_status"]
        comment_status_ = postdata_["comment_status"]
        #// Let WordPress manage slug if none was provided.
        post_name_ = postdata_["post_name"]
        if (php_isset(lambda : content_struct_["wp_slug"])):
            post_name_ = content_struct_["wp_slug"]
        # end if
        #// Only use a password if one was given.
        if (php_isset(lambda : content_struct_["wp_password"])):
            post_password_ = content_struct_["wp_password"]
        # end if
        #// Only set a post parent if one was given.
        if (php_isset(lambda : content_struct_["wp_page_parent_id"])):
            post_parent_ = content_struct_["wp_page_parent_id"]
        # end if
        #// Only set the 'menu_order' if it was given.
        if (php_isset(lambda : content_struct_["wp_page_order"])):
            menu_order_ = content_struct_["wp_page_order"]
        # end if
        page_template_ = None
        if (not php_empty(lambda : content_struct_["wp_page_template"])) and "page" == post_type_:
            page_template_ = content_struct_["wp_page_template"]
        # end if
        post_author_ = postdata_["post_author"]
        #// If an author id was provided then use it instead.
        if (php_isset(lambda : content_struct_["wp_author_id"])):
            #// Check permissions if attempting to switch author to or from another user.
            if user_.ID != content_struct_["wp_author_id"] or user_.ID != post_author_:
                for case in Switch(post_type_):
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
                post_author_ = content_struct_["wp_author_id"]
            # end if
        # end if
        if (php_isset(lambda : content_struct_["mt_allow_comments"])):
            if (not php_is_numeric(content_struct_["mt_allow_comments"])):
                for case in Switch(content_struct_["mt_allow_comments"]):
                    if case("closed"):
                        comment_status_ = "closed"
                        break
                    # end if
                    if case("open"):
                        comment_status_ = "open"
                        break
                    # end if
                    if case():
                        comment_status_ = get_default_comment_status(post_type_)
                        break
                    # end if
                # end for
            else:
                for case in Switch(php_int(content_struct_["mt_allow_comments"])):
                    if case(0):
                        pass
                    # end if
                    if case(2):
                        comment_status_ = "closed"
                        break
                    # end if
                    if case(1):
                        comment_status_ = "open"
                        break
                    # end if
                    if case():
                        comment_status_ = get_default_comment_status(post_type_)
                        break
                    # end if
                # end for
            # end if
        # end if
        if (php_isset(lambda : content_struct_["mt_allow_pings"])):
            if (not php_is_numeric(content_struct_["mt_allow_pings"])):
                for case in Switch(content_struct_["mt_allow_pings"]):
                    if case("closed"):
                        ping_status_ = "closed"
                        break
                    # end if
                    if case("open"):
                        ping_status_ = "open"
                        break
                    # end if
                    if case():
                        ping_status_ = get_default_comment_status(post_type_, "pingback")
                        break
                    # end if
                # end for
            else:
                for case in Switch(php_int(content_struct_["mt_allow_pings"])):
                    if case(0):
                        ping_status_ = "closed"
                        break
                    # end if
                    if case(1):
                        ping_status_ = "open"
                        break
                    # end if
                    if case():
                        ping_status_ = get_default_comment_status(post_type_, "pingback")
                        break
                    # end if
                # end for
            # end if
        # end if
        if (php_isset(lambda : content_struct_["title"])):
            post_title_ = content_struct_["title"]
        # end if
        if (php_isset(lambda : content_struct_["description"])):
            post_content_ = content_struct_["description"]
        # end if
        post_category_ = Array()
        if (php_isset(lambda : content_struct_["categories"])):
            catnames_ = content_struct_["categories"]
            if php_is_array(catnames_):
                for cat_ in catnames_:
                    post_category_[-1] = get_cat_ID(cat_)
                # end for
            # end if
        # end if
        if (php_isset(lambda : content_struct_["mt_excerpt"])):
            post_excerpt_ = content_struct_["mt_excerpt"]
        # end if
        post_more_ = content_struct_["mt_text_more"] if (php_isset(lambda : content_struct_["mt_text_more"])) else None
        post_status_ = "publish" if publish_ else "draft"
        if (php_isset(lambda : content_struct_[str(post_type_) + str("_status")])):
            for case in Switch(content_struct_[str(post_type_) + str("_status")]):
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
                    post_status_ = content_struct_[str(post_type_) + str("_status")]
                    break
                # end if
                if case():
                    post_status_ = "publish" if publish_ else "draft"
                    break
                # end if
            # end for
        # end if
        tags_input_ = content_struct_["mt_keywords"] if (php_isset(lambda : content_struct_["mt_keywords"])) else None
        if "publish" == post_status_ or "private" == post_status_:
            if "page" == post_type_ and (not current_user_can("publish_pages")):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this page.")))
            elif (not current_user_can("publish_posts")):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this post.")))
            # end if
        # end if
        if post_more_:
            post_content_ = post_content_ + "<!--more-->" + post_more_
        # end if
        to_ping_ = None
        if (php_isset(lambda : content_struct_["mt_tb_ping_urls"])):
            to_ping_ = content_struct_["mt_tb_ping_urls"]
            if php_is_array(to_ping_):
                to_ping_ = php_implode(" ", to_ping_)
            # end if
        # end if
        #// Do some timestamp voodoo.
        if (not php_empty(lambda : content_struct_["date_created_gmt"])):
            #// We know this is supposed to be GMT, so we're going to slap that Z on there by force.
            dateCreated_ = php_rtrim(content_struct_["date_created_gmt"].getiso(), "Z") + "Z"
        elif (not php_empty(lambda : content_struct_["dateCreated"])):
            dateCreated_ = content_struct_["dateCreated"].getiso()
        # end if
        #// Default to not flagging the post date to be edited unless it's intentional.
        edit_date_ = False
        if (not php_empty(lambda : dateCreated_)):
            post_date_ = iso8601_to_datetime(dateCreated_)
            post_date_gmt_ = iso8601_to_datetime(dateCreated_, "gmt")
            #// Flag the post date to be edited.
            edit_date_ = True
        else:
            post_date_ = postdata_["post_date"]
            post_date_gmt_ = postdata_["post_date_gmt"]
        # end if
        #// We've got all the data -- post it.
        newpost_ = php_compact("ID", "post_content", "post_title", "post_category", "post_status", "post_excerpt", "comment_status", "ping_status", "edit_date", "post_date", "post_date_gmt", "to_ping", "post_name", "post_password", "post_parent", "menu_order", "post_author", "tags_input", "page_template")
        result_ = wp_update_post(newpost_, True)
        if is_wp_error(result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, result_.get_error_message()))
        # end if
        if (not result_):
            return php_new_class("IXR_Error", lambda : IXR_Error(500, __("Sorry, the post could not be updated.")))
        # end if
        #// Only posts can be sticky.
        if "post" == post_type_ and (php_isset(lambda : content_struct_["sticky"])):
            data_ = newpost_
            data_["sticky"] = content_struct_["sticky"]
            data_["post_type"] = "post"
            error_ = self._toggle_sticky(data_, True)
            if error_:
                return error_
            # end if
        # end if
        if (php_isset(lambda : content_struct_["custom_fields"])):
            self.set_custom_fields(post_ID_, content_struct_["custom_fields"])
        # end if
        if (php_isset(lambda : content_struct_["wp_post_thumbnail"])):
            #// Empty value deletes, non-empty value adds/updates.
            if php_empty(lambda : content_struct_["wp_post_thumbnail"]):
                delete_post_thumbnail(post_ID_)
            else:
                if set_post_thumbnail(post_ID_, content_struct_["wp_post_thumbnail"]) == False:
                    return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid attachment ID.")))
                # end if
            # end if
            content_struct_["wp_post_thumbnail"] = None
        # end if
        #// Handle enclosures.
        thisEnclosure_ = content_struct_["enclosure"] if (php_isset(lambda : content_struct_["enclosure"])) else None
        self.add_enclosure_if_new(post_ID_, thisEnclosure_)
        self.attach_uploads(ID_, post_content_)
        #// Handle post formats if assigned, validation is handled earlier in this function.
        if (php_isset(lambda : content_struct_["wp_post_format"])):
            set_post_format(post_ID_, content_struct_["wp_post_format"])
        # end if
        #// 
        #// Fires after a post has been successfully updated via the XML-RPC MovableType API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $post_ID ID of the updated post.
        #// @param array $args    An array of arguments to update the post.
        #//
        do_action("xmlrpc_call_success_mw_editPost", post_ID_, args_)
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
    def mw_getpost(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[0])
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        postdata_ = get_post(post_ID_, ARRAY_A)
        if (not postdata_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.getPost")
        if "" != postdata_["post_date"]:
            post_date_ = self._convert_date(postdata_["post_date"])
            post_date_gmt_ = self._convert_date_gmt(postdata_["post_date_gmt"], postdata_["post_date"])
            post_modified_ = self._convert_date(postdata_["post_modified"])
            post_modified_gmt_ = self._convert_date_gmt(postdata_["post_modified_gmt"], postdata_["post_modified"])
            categories_ = Array()
            catids_ = wp_get_post_categories(post_ID_)
            for catid_ in catids_:
                categories_[-1] = get_cat_name(catid_)
            # end for
            tagnames_ = Array()
            tags_ = wp_get_post_tags(post_ID_)
            if (not php_empty(lambda : tags_)):
                for tag_ in tags_:
                    tagnames_[-1] = tag_.name
                # end for
                tagnames_ = php_implode(", ", tagnames_)
            else:
                tagnames_ = ""
            # end if
            post_ = get_extended(postdata_["post_content"])
            link_ = get_permalink(postdata_["ID"])
            #// Get the author info.
            author_ = get_userdata(postdata_["post_author"])
            allow_comments_ = 1 if "open" == postdata_["comment_status"] else 0
            allow_pings_ = 1 if "open" == postdata_["ping_status"] else 0
            #// Consider future posts as published.
            if "future" == postdata_["post_status"]:
                postdata_["post_status"] = "publish"
            # end if
            #// Get post format.
            post_format_ = get_post_format(post_ID_)
            if php_empty(lambda : post_format_):
                post_format_ = "standard"
            # end if
            sticky_ = False
            if is_sticky(post_ID_):
                sticky_ = True
            # end if
            enclosure_ = Array()
            for key_,val_ in get_post_custom(post_ID_):
                if "enclosure" == key_:
                    for enc_ in val_:
                        encdata_ = php_explode("\n", enc_)
                        enclosure_["url"] = php_trim(htmlspecialchars(encdata_[0]))
                        enclosure_["length"] = php_int(php_trim(encdata_[1]))
                        enclosure_["type"] = php_trim(encdata_[2])
                        break
                    # end for
                # end if
            # end for
            resp_ = Array({"dateCreated": post_date_, "userid": postdata_["post_author"], "postid": postdata_["ID"], "description": post_["main"], "title": postdata_["post_title"], "link": link_, "permaLink": link_, "categories": categories_, "mt_excerpt": postdata_["post_excerpt"], "mt_text_more": post_["extended"], "wp_more_text": post_["more_text"], "mt_allow_comments": allow_comments_, "mt_allow_pings": allow_pings_, "mt_keywords": tagnames_, "wp_slug": postdata_["post_name"], "wp_password": postdata_["post_password"], "wp_author_id": php_str(author_.ID), "wp_author_display_name": author_.display_name, "date_created_gmt": post_date_gmt_, "post_status": postdata_["post_status"], "custom_fields": self.get_custom_fields(post_ID_), "wp_post_format": post_format_, "sticky": sticky_, "date_modified": post_modified_, "date_modified_gmt": post_modified_gmt_})
            if (not php_empty(lambda : enclosure_)):
                resp_["enclosure"] = enclosure_
            # end if
            resp_["wp_post_thumbnail"] = get_post_thumbnail_id(postdata_["ID"])
            return resp_
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
    def mw_getrecentposts(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        if (php_isset(lambda : args_[3])):
            query_ = Array({"numberposts": absint(args_[3])})
        else:
            query_ = Array()
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit posts.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.getRecentPosts")
        posts_list_ = wp_get_recent_posts(query_)
        if (not posts_list_):
            return Array()
        # end if
        recent_posts_ = Array()
        for entry_ in posts_list_:
            if (not current_user_can("edit_post", entry_["ID"])):
                continue
            # end if
            post_date_ = self._convert_date(entry_["post_date"])
            post_date_gmt_ = self._convert_date_gmt(entry_["post_date_gmt"], entry_["post_date"])
            post_modified_ = self._convert_date(entry_["post_modified"])
            post_modified_gmt_ = self._convert_date_gmt(entry_["post_modified_gmt"], entry_["post_modified"])
            categories_ = Array()
            catids_ = wp_get_post_categories(entry_["ID"])
            for catid_ in catids_:
                categories_[-1] = get_cat_name(catid_)
            # end for
            tagnames_ = Array()
            tags_ = wp_get_post_tags(entry_["ID"])
            if (not php_empty(lambda : tags_)):
                for tag_ in tags_:
                    tagnames_[-1] = tag_.name
                # end for
                tagnames_ = php_implode(", ", tagnames_)
            else:
                tagnames_ = ""
            # end if
            post_ = get_extended(entry_["post_content"])
            link_ = get_permalink(entry_["ID"])
            #// Get the post author info.
            author_ = get_userdata(entry_["post_author"])
            allow_comments_ = 1 if "open" == entry_["comment_status"] else 0
            allow_pings_ = 1 if "open" == entry_["ping_status"] else 0
            #// Consider future posts as published.
            if "future" == entry_["post_status"]:
                entry_["post_status"] = "publish"
            # end if
            #// Get post format.
            post_format_ = get_post_format(entry_["ID"])
            if php_empty(lambda : post_format_):
                post_format_ = "standard"
            # end if
            recent_posts_[-1] = Array({"dateCreated": post_date_, "userid": entry_["post_author"], "postid": php_str(entry_["ID"]), "description": post_["main"], "title": entry_["post_title"], "link": link_, "permaLink": link_, "categories": categories_, "mt_excerpt": entry_["post_excerpt"], "mt_text_more": post_["extended"], "wp_more_text": post_["more_text"], "mt_allow_comments": allow_comments_, "mt_allow_pings": allow_pings_, "mt_keywords": tagnames_, "wp_slug": entry_["post_name"], "wp_password": entry_["post_password"], "wp_author_id": php_str(author_.ID), "wp_author_display_name": author_.display_name, "date_created_gmt": post_date_gmt_, "post_status": entry_["post_status"], "custom_fields": self.get_custom_fields(entry_["ID"]), "wp_post_format": post_format_, "date_modified": post_modified_, "date_modified_gmt": post_modified_gmt_, "sticky": "post" == entry_["post_type"] and is_sticky(entry_["ID"]), "wp_post_thumbnail": get_post_thumbnail_id(entry_["ID"])})
        # end for
        return recent_posts_
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
    def mw_getcategories(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view categories.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "metaWeblog.getCategories")
        categories_struct_ = Array()
        cats_ = get_categories(Array({"get": "all"}))
        if cats_:
            for cat_ in cats_:
                struct_ = Array()
                struct_["categoryId"] = cat_.term_id
                struct_["parentId"] = cat_.parent
                struct_["description"] = cat_.name
                struct_["categoryDescription"] = cat_.description
                struct_["categoryName"] = cat_.name
                struct_["htmlUrl"] = esc_html(get_category_link(cat_.term_id))
                struct_["rssUrl"] = esc_html(get_category_feed_link(cat_.term_id, "rss2"))
                categories_struct_[-1] = struct_
            # end for
        # end if
        return categories_struct_
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
    def mw_newmediaobject(self, args_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        username_ = self.escape(args_[1])
        password_ = self.escape(args_[2])
        data_ = args_[3]
        name_ = sanitize_file_name(data_["name"])
        type_ = data_["type"]
        bits_ = data_["bits"]
        user_ = self.login(username_, password_)
        if (not user_):
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
        upload_err_ = apply_filters("pre_upload_error", False)
        if upload_err_:
            return php_new_class("IXR_Error", lambda : IXR_Error(500, upload_err_))
        # end if
        upload_ = wp_upload_bits(name_, None, bits_)
        if (not php_empty(lambda : upload_["error"])):
            #// translators: 1: File name, 2: Error message.
            errorString_ = php_sprintf(__("Could not write file %1$s (%2$s)."), name_, upload_["error"])
            return php_new_class("IXR_Error", lambda : IXR_Error(500, errorString_))
        # end if
        #// Construct the attachment array.
        post_id_ = 0
        if (not php_empty(lambda : data_["post_id"])):
            post_id_ = php_int(data_["post_id"])
            if (not current_user_can("edit_post", post_id_)):
                return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
            # end if
        # end if
        attachment_ = Array({"post_title": name_, "post_content": "", "post_type": "attachment", "post_parent": post_id_, "post_mime_type": type_, "guid": upload_["url"]})
        #// Save the data.
        id_ = wp_insert_attachment(attachment_, upload_["file"], post_id_)
        wp_update_attachment_metadata(id_, wp_generate_attachment_metadata(id_, upload_["file"]))
        #// 
        #// Fires after a new attachment has been added via the XML-RPC MovableType API.
        #// 
        #// @since 3.4.0
        #// 
        #// @param int   $id   ID of the new attachment.
        #// @param array $args An array of arguments to add the attachment.
        #//
        do_action("xmlrpc_call_success_mw_newMediaObject", id_, args_)
        #// phpcs:ignore WordPress.NamingConventions.ValidHookName.NotLowercase
        struct_ = self._prepare_media_item(get_post(id_))
        #// Deprecated values.
        struct_["id"] = struct_["attachment_id"]
        struct_["file"] = struct_["title"]
        struct_["url"] = struct_["link"]
        return struct_
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
    def mt_getrecentposttitles(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        if (php_isset(lambda : args_[3])):
            query_ = Array({"numberposts": absint(args_[3])})
        else:
            query_ = Array()
        # end if
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getRecentPostTitles")
        posts_list_ = wp_get_recent_posts(query_)
        if (not posts_list_):
            self.error = php_new_class("IXR_Error", lambda : IXR_Error(500, __("Either there are no posts, or something went wrong.")))
            return self.error
        # end if
        recent_posts_ = Array()
        for entry_ in posts_list_:
            if (not current_user_can("edit_post", entry_["ID"])):
                continue
            # end if
            post_date_ = self._convert_date(entry_["post_date"])
            post_date_gmt_ = self._convert_date_gmt(entry_["post_date_gmt"], entry_["post_date"])
            recent_posts_[-1] = Array({"dateCreated": post_date_, "userid": entry_["post_author"], "postid": php_str(entry_["ID"]), "title": entry_["post_title"], "post_status": entry_["post_status"], "date_created_gmt": post_date_gmt_})
        # end for
        return recent_posts_
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
    def mt_getcategorylist(self, args_=None):
        
        
        self.escape(args_)
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not current_user_can("edit_posts")):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you must be able to edit posts on this site in order to view categories.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getCategoryList")
        categories_struct_ = Array()
        cats_ = get_categories(Array({"hide_empty": 0, "hierarchical": 0}))
        if cats_:
            for cat_ in cats_:
                struct_ = Array()
                struct_["categoryId"] = cat_.term_id
                struct_["categoryName"] = cat_.name
                categories_struct_[-1] = struct_
            # end for
        # end if
        return categories_struct_
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
    def mt_getpostcategories(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[0])
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        if (not get_post(post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getPostCategories")
        categories_ = Array()
        catids_ = wp_get_post_categories(php_intval(post_ID_))
        #// First listed category will be the primary category.
        isPrimary_ = True
        for catid_ in catids_:
            categories_[-1] = Array({"categoryName": get_cat_name(catid_), "categoryId": php_str(catid_), "isPrimary": isPrimary_})
            isPrimary_ = False
        # end for
        return categories_
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
    def mt_setpostcategories(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[0])
        username_ = args_[1]
        password_ = args_[2]
        categories_ = args_[3]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.setPostCategories")
        if (not get_post(post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to edit this post.")))
        # end if
        catids_ = Array()
        for cat_ in categories_:
            catids_[-1] = cat_["categoryId"]
        # end for
        wp_set_post_categories(post_ID_, catids_)
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
    def mt_gettrackbackpings(self, post_ID_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.getTrackbackPings")
        actual_post_ = get_post(post_ID_, ARRAY_A)
        if (not actual_post_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Sorry, no such post.")))
        # end if
        comments_ = wpdb_.get_results(wpdb_.prepare(str("SELECT comment_author_url, comment_content, comment_author_IP, comment_type FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d"), post_ID_))
        if (not comments_):
            return Array()
        # end if
        trackback_pings_ = Array()
        for comment_ in comments_:
            if "trackback" == comment_.comment_type:
                content_ = comment_.comment_content
                title_ = php_substr(content_, 8, php_strpos(content_, "</strong>") - 8)
                trackback_pings_[-1] = Array({"pingTitle": title_, "pingURL": comment_.comment_author_url, "pingIP": comment_.comment_author_IP})
            # end if
        # end for
        return trackback_pings_
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
    def mt_publishpost(self, args_=None):
        
        
        self.escape(args_)
        post_ID_ = php_int(args_[0])
        username_ = args_[1]
        password_ = args_[2]
        user_ = self.login(username_, password_)
        if (not user_):
            return self.error
        # end if
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "mt.publishPost")
        postdata_ = get_post(post_ID_, ARRAY_A)
        if (not postdata_):
            return php_new_class("IXR_Error", lambda : IXR_Error(404, __("Invalid post ID.")))
        # end if
        if (not current_user_can("publish_posts")) or (not current_user_can("edit_post", post_ID_)):
            return php_new_class("IXR_Error", lambda : IXR_Error(401, __("Sorry, you are not allowed to publish this post.")))
        # end if
        postdata_["post_status"] = "publish"
        #// Retain old categories.
        postdata_["post_category"] = wp_get_post_categories(post_ID_)
        self.escape(postdata_)
        return wp_update_post(postdata_)
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
    def pingback_ping(self, args_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "pingback.ping")
        self.escape(args_)
        pagelinkedfrom_ = php_str_replace("&amp;", "&", args_[0])
        pagelinkedto_ = php_str_replace("&amp;", "&", args_[1])
        pagelinkedto_ = php_str_replace("&", "&amp;", pagelinkedto_)
        #// 
        #// Filters the pingback source URI.
        #// 
        #// @since 3.6.0
        #// 
        #// @param string $pagelinkedfrom URI of the page linked from.
        #// @param string $pagelinkedto   URI of the page linked to.
        #//
        pagelinkedfrom_ = apply_filters("pingback_ping_source_uri", pagelinkedfrom_, pagelinkedto_)
        if (not pagelinkedfrom_):
            return self.pingback_error(0, __("A valid URL was not provided."))
        # end if
        #// Check if the page linked to is on our site.
        pos1_ = php_strpos(pagelinkedto_, php_str_replace(Array("http://www.", "http://", "https://www.", "https://"), "", get_option("home")))
        if (not pos1_):
            return self.pingback_error(0, __("Is there no link to us?"))
        # end if
        #// 
        #// Let's find which post is linked to.
        #// FIXME: Does url_to_postid() cover all these cases already?
        #// If so, then let's use it and drop the old code.
        #//
        urltest_ = php_parse_url(pagelinkedto_)
        post_ID_ = url_to_postid(pagelinkedto_)
        if post_ID_:
            pass
        elif (php_isset(lambda : urltest_["path"])) and php_preg_match("#p/[0-9]{1,}#", urltest_["path"], match_):
            #// The path defines the post_ID (archives/p/XXXX).
            blah_ = php_explode("/", match_[0])
            post_ID_ = php_int(blah_[1])
        elif (php_isset(lambda : urltest_["query"])) and php_preg_match("#p=[0-9]{1,}#", urltest_["query"], match_):
            #// The query string defines the post_ID (?p=XXXX).
            blah_ = php_explode("=", match_[0])
            post_ID_ = php_int(blah_[1])
        elif (php_isset(lambda : urltest_["fragment"])):
            #// An #anchor is there, it's either...
            if php_intval(urltest_["fragment"]):
                #// ...an integer #XXXX (simplest case),
                post_ID_ = php_int(urltest_["fragment"])
            elif php_preg_match("/post-[0-9]+/", urltest_["fragment"]):
                #// ...a post ID in the form 'post-###',
                post_ID_ = php_preg_replace("/[^0-9]+/", "", urltest_["fragment"])
            elif php_is_string(urltest_["fragment"]):
                #// ...or a string #title, a little more complicated.
                title_ = php_preg_replace("/[^a-z0-9]/i", ".", urltest_["fragment"])
                sql_ = wpdb_.prepare(str("SELECT ID FROM ") + str(wpdb_.posts) + str(" WHERE post_title RLIKE %s"), title_)
                post_ID_ = wpdb_.get_var(sql_)
                if (not post_ID_):
                    #// Returning unknown error '0' is better than die()'ing.
                    return self.pingback_error(0, "")
                # end if
            # end if
        else:
            #// TODO: Attempt to extract a post ID from the given URL.
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        post_ID_ = php_int(post_ID_)
        post_ = get_post(post_ID_)
        if (not post_):
            #// Post not found.
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        if url_to_postid(pagelinkedfrom_) == post_ID_:
            return self.pingback_error(0, __("The source URL and the target URL cannot both point to the same resource."))
        # end if
        #// Check if pings are on.
        if (not pings_open(post_)):
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        #// Let's check that the remote site didn't already pingback this entry.
        if wpdb_.get_results(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d AND comment_author_url = %s"), post_ID_, pagelinkedfrom_)):
            return self.pingback_error(48, __("The pingback has already been registered."))
        # end if
        #// Very stupid, but gives time to the 'from' server to publish!
        sleep(1)
        remote_ip_ = php_preg_replace("/[^0-9a-fA-F:., ]/", "", PHP_SERVER["REMOTE_ADDR"])
        #// This filter is documented in wp-includes/class-http.php
        user_agent_ = apply_filters("http_headers_useragent", "WordPress/" + get_bloginfo("version") + "; " + get_bloginfo("url"), pagelinkedfrom_)
        #// Let's check the remote site.
        http_api_args_ = Array({"timeout": 10, "redirection": 0, "limit_response_size": 153600, "user-agent": str(user_agent_) + str("; verifying pingback from ") + str(remote_ip_), "headers": Array({"X-Pingback-Forwarded-For": remote_ip_})})
        request_ = wp_safe_remote_get(pagelinkedfrom_, http_api_args_)
        remote_source_ = wp_remote_retrieve_body(request_)
        remote_source_original_ = remote_source_
        if (not remote_source_):
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
        remote_source_ = apply_filters("pre_remote_source", remote_source_, pagelinkedto_)
        #// Work around bug in strip_tags():
        remote_source_ = php_str_replace("<!DOC", "<DOC", remote_source_)
        remote_source_ = php_preg_replace("/[\\r\\n\\t ]+/", " ", remote_source_)
        #// normalize spaces
        remote_source_ = php_preg_replace("/<\\/*(h1|h2|h3|h4|h5|h6|p|th|td|li|dt|dd|pre|caption|input|textarea|button|body)[^>]*>/", "\n\n", remote_source_)
        php_preg_match("|<title>([^<]*?)</title>|is", remote_source_, matchtitle_)
        title_ = matchtitle_[1] if (php_isset(lambda : matchtitle_[1])) else ""
        if php_empty(lambda : title_):
            return self.pingback_error(32, __("We cannot find a title on that page."))
        # end if
        #// Remove all script and style tags including their content.
        remote_source_ = php_preg_replace("@<(script|style)[^>]*?>.*?</\\1>@si", "", remote_source_)
        #// Just keep the tag we need.
        remote_source_ = strip_tags(remote_source_, "<a>")
        p_ = php_explode("\n\n", remote_source_)
        preg_target_ = preg_quote(pagelinkedto_, "|")
        for para_ in p_:
            if php_strpos(para_, pagelinkedto_) != False:
                #// It exists, but is it a link?
                php_preg_match("|<a[^>]+?" + preg_target_ + "[^>]*>([^>]+?)</a>|", para_, context_)
                #// If the URL isn't in a link context, keep looking.
                if php_empty(lambda : context_):
                    continue
                # end if
                #// We're going to use this fake tag to mark the context in a bit.
                #// The marker is needed in case the link text appears more than once in the paragraph.
                excerpt_ = php_preg_replace("|\\</?wpcontext\\>|", "", para_)
                #// prevent really long link text
                if php_strlen(context_[1]) > 100:
                    context_[1] = php_substr(context_[1], 0, 100) + "&#8230;"
                # end if
                marker_ = "<wpcontext>" + context_[1] + "</wpcontext>"
                #// Set up our marker.
                excerpt_ = php_str_replace(context_[0], marker_, excerpt_)
                #// Swap out the link for our marker.
                excerpt_ = strip_tags(excerpt_, "<wpcontext>")
                #// Strip all tags but our context marker.
                excerpt_ = php_trim(excerpt_)
                preg_marker_ = preg_quote(marker_, "|")
                excerpt_ = php_preg_replace(str("|.*?\\s(.{0,100}") + str(preg_marker_) + str(".{0,100})\\s.*|s"), "$1", excerpt_)
                excerpt_ = strip_tags(excerpt_)
                break
            # end if
        # end for
        if php_empty(lambda : context_):
            #// Link to target not found.
            return self.pingback_error(17, __("The source URL does not contain a link to the target URL, and so cannot be used as a source."))
        # end if
        pagelinkedfrom_ = php_str_replace("&", "&amp;", pagelinkedfrom_)
        context_ = "[&#8230;] " + esc_html(excerpt_) + " [&#8230;]"
        pagelinkedfrom_ = self.escape(pagelinkedfrom_)
        comment_post_ID_ = php_int(post_ID_)
        comment_author_ = title_
        comment_author_email_ = ""
        self.escape(comment_author_)
        comment_author_url_ = pagelinkedfrom_
        comment_content_ = context_
        self.escape(comment_content_)
        comment_type_ = "pingback"
        commentdata_ = php_compact("comment_post_ID", "comment_author", "comment_author_url", "comment_author_email", "comment_content", "comment_type", "remote_source", "remote_source_original")
        comment_ID_ = wp_new_comment(commentdata_)
        if is_wp_error(comment_ID_):
            return self.pingback_error(0, comment_ID_.get_error_message())
        # end if
        #// 
        #// Fires after a post pingback has been sent.
        #// 
        #// @since 0.71
        #// 
        #// @param int $comment_ID Comment ID.
        #//
        do_action("pingback_post", comment_ID_)
        #// translators: 1: URL of the page linked from, 2: URL of the page linked to.
        return php_sprintf(__("Pingback from %1$s to %2$s registered. Keep the web talking! :-)"), pagelinkedfrom_, pagelinkedto_)
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
    def pingback_extensions_getpingbacks(self, url_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        #// This action is documented in wp-includes/class-wp-xmlrpc-server.php
        do_action("xmlrpc_call", "pingback.extensions.getPingbacks")
        url_ = self.escape(url_)
        post_ID_ = url_to_postid(url_)
        if (not post_ID_):
            #// We aren't sure that the resource is available and/or pingback enabled.
            return self.pingback_error(33, __("The specified target URL cannot be used as a target. It either doesn&#8217;t exist, or it is not a pingback-enabled resource."))
        # end if
        actual_post_ = get_post(post_ID_, ARRAY_A)
        if (not actual_post_):
            #// No such post = resource not found.
            return self.pingback_error(32, __("The specified target URL does not exist."))
        # end if
        comments_ = wpdb_.get_results(wpdb_.prepare(str("SELECT comment_author_url, comment_content, comment_author_IP, comment_type FROM ") + str(wpdb_.comments) + str(" WHERE comment_post_ID = %d"), post_ID_))
        if (not comments_):
            return Array()
        # end if
        pingbacks_ = Array()
        for comment_ in comments_:
            if "pingback" == comment_.comment_type:
                pingbacks_[-1] = comment_.comment_author_url
            # end if
        # end for
        return pingbacks_
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
    def pingback_error(self, code_=None, message_=None):
        
        
        #// 
        #// Filters the XML-RPC pingback error return.
        #// 
        #// @since 3.5.1
        #// 
        #// @param IXR_Error $error An IXR_Error object containing the error code and message.
        #//
        return apply_filters("xmlrpc_pingback_error", php_new_class("IXR_Error", lambda : IXR_Error(code_, message_)))
    # end def pingback_error
# end class wp_xmlrpc_server
