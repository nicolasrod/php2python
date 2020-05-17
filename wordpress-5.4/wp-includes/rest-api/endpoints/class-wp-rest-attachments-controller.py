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
#// REST API: WP_REST_Attachments_Controller class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.7.0
#// 
#// 
#// Core controller used to access attachments via the REST API.
#// 
#// @since 4.7.0
#// 
#// @see WP_REST_Posts_Controller
#//
class WP_REST_Attachments_Controller(WP_REST_Posts_Controller):
    #// 
    #// Registers the routes for attachments.
    #// 
    #// @since 5.3.0
    #// 
    #// @see register_rest_route()
    #//
    def register_routes(self):
        
        
        super().register_routes()
        register_rest_route(self.namespace, "/" + self.rest_base + "/(?P<id>[\\d]+)/post-process", Array({"methods": WP_REST_Server.CREATABLE, "callback": Array(self, "post_process_item"), "permission_callback": Array(self, "post_process_item_permissions_check"), "args": Array({"id": Array({"description": __("Unique identifier for the object."), "type": "integer"})}, {"action": Array({"type": "string", "enum": Array("create-image-subsizes"), "required": True})})}))
    # end def register_routes
    #// 
    #// Determines the allowed query_vars for a get_items() response and
    #// prepares for WP_Query.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array           $prepared_args Optional. Array of prepared arguments. Default empty array.
    #// @param WP_REST_Request $request       Optional. Request to prepare items for.
    #// @return array Array of query arguments.
    #//
    def prepare_items_query(self, prepared_args_=None, request_=None):
        if prepared_args_ is None:
            prepared_args_ = Array()
        # end if
        
        query_args_ = super().prepare_items_query(prepared_args_, request_)
        if php_empty(lambda : query_args_["post_status"]):
            query_args_["post_status"] = "inherit"
        # end if
        media_types_ = self.get_media_types()
        if (not php_empty(lambda : request_["media_type"])) and (php_isset(lambda : media_types_[request_["media_type"]])):
            query_args_["post_mime_type"] = media_types_[request_["media_type"]]
        # end if
        if (not php_empty(lambda : request_["mime_type"])):
            parts_ = php_explode("/", request_["mime_type"])
            if (php_isset(lambda : media_types_[parts_[0]])) and php_in_array(request_["mime_type"], media_types_[parts_[0]], True):
                query_args_["post_mime_type"] = request_["mime_type"]
            # end if
        # end if
        #// Filter query clauses to include filenames.
        if (php_isset(lambda : query_args_["s"])):
            add_filter("posts_clauses", "_filter_query_attachment_filenames")
        # end if
        return query_args_
    # end def prepare_items_query
    #// 
    #// Checks if a given request has access to create an attachment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error Boolean true if the attachment may be created, or a WP_Error if not.
    #//
    def create_item_permissions_check(self, request_=None):
        
        
        ret_ = super().create_item_permissions_check(request_)
        if (not ret_) or is_wp_error(ret_):
            return ret_
        # end if
        if (not current_user_can("upload_files")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_create", __("Sorry, you are not allowed to upload media on this site."), Array({"status": 400})))
        # end if
        #// Attaching media to a post requires ability to edit said post.
        if (not php_empty(lambda : request_["post"])):
            parent_ = get_post(php_int(request_["post"]))
            post_parent_type_ = get_post_type_object(parent_.post_type)
            if (not current_user_can(post_parent_type_.cap.edit_post, request_["post"])):
                return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_edit", __("Sorry, you are not allowed to upload media to this post."), Array({"status": rest_authorization_required_code()})))
            # end if
        # end if
        return True
    # end def create_item_permissions_check
    #// 
    #// Creates a single attachment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, WP_Error object on failure.
    #//
    def create_item(self, request_=None):
        
        
        if (not php_empty(lambda : request_["post"])) and php_in_array(get_post_type(request_["post"]), Array("revision", "attachment"), True):
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid parent type."), Array({"status": 400})))
        # end if
        insert_ = self.insert_attachment(request_)
        if is_wp_error(insert_):
            return insert_
        # end if
        schema_ = self.get_item_schema()
        #// Extract by name.
        attachment_id_ = insert_["attachment_id"]
        file_ = insert_["file"]
        if (php_isset(lambda : request_["alt_text"])):
            update_post_meta(attachment_id_, "_wp_attachment_image_alt", sanitize_text_field(request_["alt_text"]))
        # end if
        if (not php_empty(lambda : schema_["properties"]["meta"])) and (php_isset(lambda : request_["meta"])):
            meta_update_ = self.meta.update_value(request_["meta"], attachment_id_)
            if is_wp_error(meta_update_):
                return meta_update_
            # end if
        # end if
        attachment_ = get_post(attachment_id_)
        fields_update_ = self.update_additional_fields_for_object(attachment_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// 
        #// Fires after a single attachment is completely created or updated via the REST API.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_Post         $attachment Inserted or updated attachment object.
        #// @param WP_REST_Request $request    Request object.
        #// @param bool            $creating   True when creating an attachment, false when updating.
        #//
        do_action("rest_after_insert_attachment", attachment_, request_, True)
        if php_defined("REST_REQUEST") and REST_REQUEST:
            #// Set a custom header with the attachment_id.
            #// Used by the browser/client to resume creating image sub-sizes after a PHP fatal error.
            php_header("X-WP-Upload-Attachment-ID: " + attachment_id_)
        # end if
        #// Include media and image functions to get access to wp_generate_attachment_metadata().
        php_include_file(ABSPATH + "wp-admin/includes/media.php", once=True)
        php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
        #// Post-process the upload (create image sub-sizes, make PDF thumbnails, etc.) and insert attachment meta.
        #// At this point the server may run out of resources and post-processing of uploaded images may fail.
        wp_update_attachment_metadata(attachment_id_, wp_generate_attachment_metadata(attachment_id_, file_))
        response_ = self.prepare_item_for_response(attachment_, request_)
        response_ = rest_ensure_response(response_)
        response_.set_status(201)
        response_.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, attachment_id_)))
        return response_
    # end def create_item
    #// 
    #// Inserts the attachment post in the database. Does not update the attachment meta.
    #// 
    #// @since 5.3.0
    #// 
    #// @param WP_REST_Request $request
    #// @return array|WP_Error
    #//
    def insert_attachment(self, request_=None):
        
        
        #// Get the file via $_FILES or raw data.
        files_ = request_.get_file_params()
        headers_ = request_.get_headers()
        if (not php_empty(lambda : files_)):
            file_ = self.upload_from_file(files_, headers_)
        else:
            file_ = self.upload_from_data(request_.get_body(), headers_)
        # end if
        if is_wp_error(file_):
            return file_
        # end if
        name_ = wp_basename(file_["file"])
        name_parts_ = pathinfo(name_)
        name_ = php_trim(php_substr(name_, 0, -1 + php_strlen(name_parts_["extension"])))
        url_ = file_["url"]
        type_ = file_["type"]
        file_ = file_["file"]
        #// Include image functions to get access to wp_read_image_metadata().
        php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
        #// Use image exif/iptc data for title and caption defaults if possible.
        image_meta_ = wp_read_image_metadata(file_)
        if (not php_empty(lambda : image_meta_)):
            if php_empty(lambda : request_["title"]) and php_trim(image_meta_["title"]) and (not php_is_numeric(sanitize_title(image_meta_["title"]))):
                request_["title"] = image_meta_["title"]
            # end if
            if php_empty(lambda : request_["caption"]) and php_trim(image_meta_["caption"]):
                request_["caption"] = image_meta_["caption"]
            # end if
        # end if
        attachment_ = self.prepare_item_for_database(request_)
        attachment_.post_mime_type = type_
        attachment_.guid = url_
        if php_empty(lambda : attachment_.post_title):
            attachment_.post_title = php_preg_replace("/\\.[^.]+$/", "", wp_basename(file_))
        # end if
        #// $post_parent is inherited from $attachment['post_parent'].
        id_ = wp_insert_attachment(wp_slash(attachment_), file_, 0, True)
        if is_wp_error(id_):
            if "db_update_error" == id_.get_error_code():
                id_.add_data(Array({"status": 500}))
            else:
                id_.add_data(Array({"status": 400}))
            # end if
            return id_
        # end if
        attachment_ = get_post(id_)
        #// 
        #// Fires after a single attachment is created or updated via the REST API.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_Post         $attachment Inserted or updated attachment
        #// object.
        #// @param WP_REST_Request $request    The request sent to the API.
        #// @param bool            $creating   True when creating an attachment, false when updating.
        #//
        do_action("rest_insert_attachment", attachment_, request_, True)
        return Array({"attachment_id": id_, "file": file_})
    # end def insert_attachment
    #// 
    #// Updates a single attachment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, WP_Error object on failure.
    #//
    def update_item(self, request_=None):
        
        
        if (not php_empty(lambda : request_["post"])) and php_in_array(get_post_type(request_["post"]), Array("revision", "attachment"), True):
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid parent type."), Array({"status": 400})))
        # end if
        response_ = super().update_item(request_)
        if is_wp_error(response_):
            return response_
        # end if
        response_ = rest_ensure_response(response_)
        data_ = response_.get_data()
        if (php_isset(lambda : request_["alt_text"])):
            update_post_meta(data_["id"], "_wp_attachment_image_alt", request_["alt_text"])
        # end if
        attachment_ = get_post(request_["id"])
        fields_update_ = self.update_additional_fields_for_object(attachment_, request_)
        if is_wp_error(fields_update_):
            return fields_update_
        # end if
        request_.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-attachments-controller.php
        do_action("rest_after_insert_attachment", attachment_, request_, False)
        response_ = self.prepare_item_for_response(attachment_, request_)
        response_ = rest_ensure_response(response_)
        return response_
    # end def update_item
    #// 
    #// Performs post processing on an attachment.
    #// 
    #// @since 5.3.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, WP_Error object on failure.
    #//
    def post_process_item(self, request_=None):
        
        
        for case in Switch(request_["action"]):
            if case("create-image-subsizes"):
                php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
                wp_update_image_subsizes(request_["id"])
                break
            # end if
        # end for
        request_["context"] = "edit"
        return self.prepare_item_for_response(get_post(request_["id"]), request_)
    # end def post_process_item
    #// 
    #// Checks if a given request can perform post processing on an attachment.
    #// 
    #// @sicne 5.3.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def post_process_item_permissions_check(self, request_=None):
        
        
        return self.update_item_permissions_check(request_)
    # end def post_process_item_permissions_check
    #// 
    #// Prepares a single attachment for create or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return stdClass|WP_Error Post object.
    #//
    def prepare_item_for_database(self, request_=None):
        
        
        prepared_attachment_ = super().prepare_item_for_database(request_)
        #// Attachment caption (post_excerpt internally).
        if (php_isset(lambda : request_["caption"])):
            if php_is_string(request_["caption"]):
                prepared_attachment_.post_excerpt = request_["caption"]
            elif (php_isset(lambda : request_["caption"]["raw"])):
                prepared_attachment_.post_excerpt = request_["caption"]["raw"]
            # end if
        # end if
        #// Attachment description (post_content internally).
        if (php_isset(lambda : request_["description"])):
            if php_is_string(request_["description"]):
                prepared_attachment_.post_content = request_["description"]
            elif (php_isset(lambda : request_["description"]["raw"])):
                prepared_attachment_.post_content = request_["description"]["raw"]
            # end if
        # end if
        if (php_isset(lambda : request_["post"])):
            prepared_attachment_.post_parent = php_int(request_["post"])
        # end if
        return prepared_attachment_
    # end def prepare_item_for_database
    #// 
    #// Prepares a single attachment output for response.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_Post         $post    Attachment object.
    #// @param WP_REST_Request $request Request object.
    #// @return WP_REST_Response Response object.
    #//
    def prepare_item_for_response(self, post_=None, request_=None):
        
        
        response_ = super().prepare_item_for_response(post_, request_)
        fields_ = self.get_fields_for_response(request_)
        data_ = response_.get_data()
        if php_in_array("description", fields_, True):
            data_["description"] = Array({"raw": post_.post_content, "rendered": apply_filters("the_content", post_.post_content)})
        # end if
        if php_in_array("caption", fields_, True):
            #// This filter is documented in wp-includes/post-template.php
            caption_ = apply_filters("get_the_excerpt", post_.post_excerpt, post_)
            #// This filter is documented in wp-includes/post-template.php
            caption_ = apply_filters("the_excerpt", caption_)
            data_["caption"] = Array({"raw": post_.post_excerpt, "rendered": caption_})
        # end if
        if php_in_array("alt_text", fields_, True):
            data_["alt_text"] = get_post_meta(post_.ID, "_wp_attachment_image_alt", True)
        # end if
        if php_in_array("media_type", fields_, True):
            data_["media_type"] = "image" if wp_attachment_is_image(post_.ID) else "file"
        # end if
        if php_in_array("mime_type", fields_, True):
            data_["mime_type"] = post_.post_mime_type
        # end if
        if php_in_array("media_details", fields_, True):
            data_["media_details"] = wp_get_attachment_metadata(post_.ID)
            #// Ensure empty details is an empty object.
            if php_empty(lambda : data_["media_details"]):
                data_["media_details"] = php_new_class("stdClass", lambda : stdClass())
            elif (not php_empty(lambda : data_["media_details"]["sizes"])):
                for size_,size_data_ in data_["media_details"]["sizes"]:
                    if (php_isset(lambda : size_data_["mime-type"])):
                        size_data_["mime_type"] = size_data_["mime-type"]
                        size_data_["mime-type"] = None
                    # end if
                    #// Use the same method image_downsize() does.
                    image_src_ = wp_get_attachment_image_src(post_.ID, size_)
                    if (not image_src_):
                        continue
                    # end if
                    size_data_["source_url"] = image_src_[0]
                # end for
                full_src_ = wp_get_attachment_image_src(post_.ID, "full")
                if (not php_empty(lambda : full_src_)):
                    data_["media_details"]["sizes"]["full"] = Array({"file": wp_basename(full_src_[0]), "width": full_src_[1], "height": full_src_[2], "mime_type": post_.post_mime_type, "source_url": full_src_[0]})
                # end if
            else:
                data_["media_details"]["sizes"] = php_new_class("stdClass", lambda : stdClass())
            # end if
        # end if
        if php_in_array("post", fields_, True):
            data_["post"] = php_int(post_.post_parent) if (not php_empty(lambda : post_.post_parent)) else None
        # end if
        if php_in_array("source_url", fields_, True):
            data_["source_url"] = wp_get_attachment_url(post_.ID)
        # end if
        if php_in_array("missing_image_sizes", fields_, True):
            php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
            data_["missing_image_sizes"] = php_array_keys(wp_get_missing_image_subsizes(post_.ID))
        # end if
        context_ = request_["context"] if (not php_empty(lambda : request_["context"])) else "view"
        data_ = self.filter_response_by_context(data_, context_)
        links_ = response_.get_links()
        #// Wrap the data in a response object.
        response_ = rest_ensure_response(data_)
        for rel_,rel_links_ in links_:
            for link_ in rel_links_:
                response_.add_link(rel_, link_["href"], link_["attributes"])
            # end for
        # end for
        #// 
        #// Filters an attachment returned from the REST API.
        #// 
        #// Allows modification of the attachment right before it is returned.
        #// 
        #// @since 4.7.0
        #// 
        #// @param WP_REST_Response $response The response object.
        #// @param WP_Post          $post     The original attachment post.
        #// @param WP_REST_Request  $request  Request used to generate the response.
        #//
        return apply_filters("rest_prepare_attachment", response_, post_, request_)
    # end def prepare_item_for_response
    #// 
    #// Retrieves the attachment's schema, conforming to JSON Schema.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Item schema as an array.
    #//
    def get_item_schema(self):
        
        
        if self.schema:
            return self.add_additional_fields_schema(self.schema)
        # end if
        schema_ = super().get_item_schema()
        schema_["properties"]["alt_text"] = Array({"description": __("Alternative text to display when attachment is not displayed."), "type": "string", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})
        schema_["properties"]["caption"] = Array({"description": __("The attachment caption."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Caption for the attachment, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML caption for the attachment, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
        schema_["properties"]["description"] = Array({"description": __("The attachment description."), "type": "object", "context": Array("view", "edit"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Description for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML description for the object, transformed for display."), "type": "string", "context": Array("view", "edit"), "readonly": True})})})
        schema_["properties"]["media_type"] = Array({"description": __("Attachment type."), "type": "string", "enum": Array("image", "file"), "context": Array("view", "edit", "embed"), "readonly": True})
        schema_["properties"]["mime_type"] = Array({"description": __("The attachment MIME type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})
        schema_["properties"]["media_details"] = Array({"description": __("Details about the media file, specific to its type."), "type": "object", "context": Array("view", "edit", "embed"), "readonly": True})
        schema_["properties"]["post"] = Array({"description": __("The ID for the associated post of the attachment."), "type": "integer", "context": Array("view", "edit")})
        schema_["properties"]["source_url"] = Array({"description": __("URL to the original attachment file."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed"), "readonly": True})
        schema_["properties"]["missing_image_sizes"] = Array({"description": __("List of the missing image sizes of the attachment."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("edit"), "readonly": True})
        schema_["properties"]["password"] = None
        self.schema = schema_
        return self.add_additional_fields_schema(self.schema)
    # end def get_item_schema
    #// 
    #// Handles an upload via raw POST data.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $data    Supplied file data.
    #// @param array $headers HTTP headers from the request.
    #// @return array|WP_Error Data from wp_handle_sideload().
    #//
    def upload_from_data(self, data_=None, headers_=None):
        
        
        if php_empty(lambda : data_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_data", __("No data supplied."), Array({"status": 400})))
        # end if
        if php_empty(lambda : headers_["content_type"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_content_type", __("No Content-Type supplied."), Array({"status": 400})))
        # end if
        if php_empty(lambda : headers_["content_disposition"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_content_disposition", __("No Content-Disposition supplied."), Array({"status": 400})))
        # end if
        filename_ = self.get_filename_from_disposition(headers_["content_disposition"])
        if php_empty(lambda : filename_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_invalid_disposition", __("Invalid Content-Disposition supplied. Content-Disposition needs to be formatted as `attachment; filename=\"image.png\"` or similar."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : headers_["content_md5"])):
            content_md5_ = php_array_shift(headers_["content_md5"])
            expected_ = php_trim(content_md5_)
            actual_ = php_md5(data_)
            if expected_ != actual_:
                return php_new_class("WP_Error", lambda : WP_Error("rest_upload_hash_mismatch", __("Content hash did not match expected."), Array({"status": 412})))
            # end if
        # end if
        #// Get the content-type.
        type_ = php_array_shift(headers_["content_type"])
        #// Include filesystem functions to get access to wp_tempnam() and wp_handle_sideload().
        php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
        #// Save the file.
        tmpfname_ = wp_tempnam(filename_)
        fp_ = fopen(tmpfname_, "w+")
        if (not fp_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_file_error", __("Could not open file handle."), Array({"status": 500})))
        # end if
        fwrite(fp_, data_)
        php_fclose(fp_)
        #// Now, sideload it in.
        file_data_ = Array({"error": None, "tmp_name": tmpfname_, "name": filename_, "type": type_})
        size_check_ = self.check_upload_size(file_data_)
        if is_wp_error(size_check_):
            return size_check_
        # end if
        overrides_ = Array({"test_form": False})
        sideloaded_ = wp_handle_sideload(file_data_, overrides_)
        if (php_isset(lambda : sideloaded_["error"])):
            php_no_error(lambda: unlink(tmpfname_))
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_sideload_error", sideloaded_["error"], Array({"status": 500})))
        # end if
        return sideloaded_
    # end def upload_from_data
    #// 
    #// Parses filename from a Content-Disposition header value.
    #// 
    #// As per RFC6266:
    #// 
    #// content-disposition = "Content-Disposition" ":"
    #// disposition-type *( ";" disposition-parm )
    #// 
    #// disposition-type    = "inline" | "attachment" | disp-ext-type
    #// ; case-insensitive
    #// disp-ext-type       = token
    #// 
    #// disposition-parm    = filename-parm | disp-ext-parm
    #// 
    #// filename-parm       = "filename" "=" value
    #// | "filename*" "=" ext-value
    #// 
    #// disp-ext-parm       = token "=" value
    #// | ext-token "=" ext-value
    #// ext-token           = <the characters in token, followed by "*">
    #// 
    #// @since 4.7.0
    #// 
    #// @link https://tools.ietf.org/html/rfc2388
    #// @link https://tools.ietf.org/html/rfc6266
    #// 
    #// @param string[] $disposition_header List of Content-Disposition header values.
    #// @return string|null Filename if available, or null if not found.
    #//
    @classmethod
    def get_filename_from_disposition(self, disposition_header_=None):
        
        
        #// Get the filename.
        filename_ = None
        for value_ in disposition_header_:
            value_ = php_trim(value_)
            if php_strpos(value_, ";") == False:
                continue
            # end if
            type_, attr_parts_ = php_explode(";", value_, 2)
            attr_parts_ = php_explode(";", attr_parts_)
            attributes_ = Array()
            for part_ in attr_parts_:
                if php_strpos(part_, "=") == False:
                    continue
                # end if
                key_, value_ = php_explode("=", part_, 2)
                attributes_[php_trim(key_)] = php_trim(value_)
            # end for
            if php_empty(lambda : attributes_["filename"]):
                continue
            # end if
            filename_ = php_trim(attributes_["filename"])
            #// Unquote quoted filename, but after trimming.
            if php_substr(filename_, 0, 1) == "\"" and php_substr(filename_, -1, 1) == "\"":
                filename_ = php_substr(filename_, 1, -1)
            # end if
        # end for
        return filename_
    # end def get_filename_from_disposition
    #// 
    #// Retrieves the query params for collections of attachments.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Query parameters for the attachment collection as an array.
    #//
    def get_collection_params(self):
        
        
        params_ = super().get_collection_params()
        params_["status"]["default"] = "inherit"
        params_["status"]["items"]["enum"] = Array("inherit", "private", "trash")
        media_types_ = self.get_media_types()
        params_["media_type"] = Array({"default": None, "description": __("Limit result set to attachments of a particular media type."), "type": "string", "enum": php_array_keys(media_types_)})
        params_["mime_type"] = Array({"default": None, "description": __("Limit result set to attachments of a particular MIME type."), "type": "string"})
        return params_
    # end def get_collection_params
    #// 
    #// Handles an upload via multipart/form-data ($_FILES).
    #// 
    #// @since 4.7.0
    #// 
    #// @param array $files   Data from the `$_FILES` superglobal.
    #// @param array $headers HTTP headers from the request.
    #// @return array|WP_Error Data from wp_handle_upload().
    #//
    def upload_from_file(self, files_=None, headers_=None):
        
        
        if php_empty(lambda : files_):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_data", __("No data supplied."), Array({"status": 400})))
        # end if
        #// Verify hash, if given.
        if (not php_empty(lambda : headers_["content_md5"])):
            content_md5_ = php_array_shift(headers_["content_md5"])
            expected_ = php_trim(content_md5_)
            actual_ = php_md5_file(files_["file"]["tmp_name"])
            if expected_ != actual_:
                return php_new_class("WP_Error", lambda : WP_Error("rest_upload_hash_mismatch", __("Content hash did not match expected."), Array({"status": 412})))
            # end if
        # end if
        #// Pass off to WP to handle the actual upload.
        overrides_ = Array({"test_form": False})
        #// Bypasses is_uploaded_file() when running unit tests.
        if php_defined("DIR_TESTDATA") and DIR_TESTDATA:
            overrides_["action"] = "wp_handle_mock_upload"
        # end if
        size_check_ = self.check_upload_size(files_["file"])
        if is_wp_error(size_check_):
            return size_check_
        # end if
        #// Include filesystem functions to get access to wp_handle_upload().
        php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
        file_ = wp_handle_upload(files_["file"], overrides_)
        if (php_isset(lambda : file_["error"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_unknown_error", file_["error"], Array({"status": 500})))
        # end if
        return file_
    # end def upload_from_file
    #// 
    #// Retrieves the supported media types.
    #// 
    #// Media types are considered the MIME type category.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Array of supported media types.
    #//
    def get_media_types(self):
        
        
        media_types_ = Array()
        for mime_type_ in get_allowed_mime_types():
            parts_ = php_explode("/", mime_type_)
            if (not (php_isset(lambda : media_types_[parts_[0]]))):
                media_types_[parts_[0]] = Array()
            # end if
            media_types_[parts_[0]][-1] = mime_type_
        # end for
        return media_types_
    # end def get_media_types
    #// 
    #// Determine if uploaded file exceeds space quota on multisite.
    #// 
    #// Replicates check_upload_size().
    #// 
    #// @since 4.9.8
    #// 
    #// @param array $file $_FILES array for a given file.
    #// @return true|WP_Error True if can upload, error for errors.
    #//
    def check_upload_size(self, file_=None):
        
        
        if (not is_multisite()):
            return True
        # end if
        if get_site_option("upload_space_check_disabled"):
            return True
        # end if
        space_left_ = get_upload_space_available()
        file_size_ = filesize(file_["tmp_name"])
        if space_left_ < file_size_:
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_limited_space", php_sprintf(__("Not enough space to upload. %s KB needed."), number_format(file_size_ - space_left_ / KB_IN_BYTES)), Array({"status": 400})))
        # end if
        if file_size_ > KB_IN_BYTES * get_site_option("fileupload_maxk", 1500):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_file_too_big", php_sprintf(__("This file is too big. Files must be less than %s KB in size."), get_site_option("fileupload_maxk", 1500)), Array({"status": 400})))
        # end if
        #// Include multisite admin functions to get access to upload_is_user_over_quota().
        php_include_file(ABSPATH + "wp-admin/includes/ms.php", once=True)
        if upload_is_user_over_quota(False):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_user_quota_exceeded", __("You have used your space quota. Please delete files before uploading."), Array({"status": 400})))
        # end if
        return True
    # end def check_upload_size
# end class WP_REST_Attachments_Controller
