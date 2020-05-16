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
    def prepare_items_query(self, prepared_args=Array(), request=None):
        
        query_args = super().prepare_items_query(prepared_args, request)
        if php_empty(lambda : query_args["post_status"]):
            query_args["post_status"] = "inherit"
        # end if
        media_types = self.get_media_types()
        if (not php_empty(lambda : request["media_type"])) and (php_isset(lambda : media_types[request["media_type"]])):
            query_args["post_mime_type"] = media_types[request["media_type"]]
        # end if
        if (not php_empty(lambda : request["mime_type"])):
            parts = php_explode("/", request["mime_type"])
            if (php_isset(lambda : media_types[parts[0]])) and php_in_array(request["mime_type"], media_types[parts[0]], True):
                query_args["post_mime_type"] = request["mime_type"]
            # end if
        # end if
        #// Filter query clauses to include filenames.
        if (php_isset(lambda : query_args["s"])):
            add_filter("posts_clauses", "_filter_query_attachment_filenames")
        # end if
        return query_args
    # end def prepare_items_query
    #// 
    #// Checks if a given request has access to create an attachment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error Boolean true if the attachment may be created, or a WP_Error if not.
    #//
    def create_item_permissions_check(self, request=None):
        
        ret = super().create_item_permissions_check(request)
        if (not ret) or is_wp_error(ret):
            return ret
        # end if
        if (not current_user_can("upload_files")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_cannot_create", __("Sorry, you are not allowed to upload media on this site."), Array({"status": 400})))
        # end if
        #// Attaching media to a post requires ability to edit said post.
        if (not php_empty(lambda : request["post"])):
            parent = get_post(php_int(request["post"]))
            post_parent_type = get_post_type_object(parent.post_type)
            if (not current_user_can(post_parent_type.cap.edit_post, request["post"])):
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
    def create_item(self, request=None):
        
        if (not php_empty(lambda : request["post"])) and php_in_array(get_post_type(request["post"]), Array("revision", "attachment"), True):
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid parent type."), Array({"status": 400})))
        # end if
        insert = self.insert_attachment(request)
        if is_wp_error(insert):
            return insert
        # end if
        schema = self.get_item_schema()
        #// Extract by name.
        attachment_id = insert["attachment_id"]
        file = insert["file"]
        if (php_isset(lambda : request["alt_text"])):
            update_post_meta(attachment_id, "_wp_attachment_image_alt", sanitize_text_field(request["alt_text"]))
        # end if
        if (not php_empty(lambda : schema["properties"]["meta"])) and (php_isset(lambda : request["meta"])):
            meta_update = self.meta.update_value(request["meta"], attachment_id)
            if is_wp_error(meta_update):
                return meta_update
            # end if
        # end if
        attachment = get_post(attachment_id)
        fields_update = self.update_additional_fields_for_object(attachment, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// 
        #// Fires after a single attachment is completely created or updated via the REST API.
        #// 
        #// @since 5.0.0
        #// 
        #// @param WP_Post         $attachment Inserted or updated attachment object.
        #// @param WP_REST_Request $request    Request object.
        #// @param bool            $creating   True when creating an attachment, false when updating.
        #//
        do_action("rest_after_insert_attachment", attachment, request, True)
        if php_defined("REST_REQUEST") and REST_REQUEST:
            #// Set a custom header with the attachment_id.
            #// Used by the browser/client to resume creating image sub-sizes after a PHP fatal error.
            php_header("X-WP-Upload-Attachment-ID: " + attachment_id)
        # end if
        #// Include media and image functions to get access to wp_generate_attachment_metadata().
        php_include_file(ABSPATH + "wp-admin/includes/media.php", once=True)
        php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
        #// Post-process the upload (create image sub-sizes, make PDF thumbnails, etc.) and insert attachment meta.
        #// At this point the server may run out of resources and post-processing of uploaded images may fail.
        wp_update_attachment_metadata(attachment_id, wp_generate_attachment_metadata(attachment_id, file))
        response = self.prepare_item_for_response(attachment, request)
        response = rest_ensure_response(response)
        response.set_status(201)
        response.header("Location", rest_url(php_sprintf("%s/%s/%d", self.namespace, self.rest_base, attachment_id)))
        return response
    # end def create_item
    #// 
    #// Inserts the attachment post in the database. Does not update the attachment meta.
    #// 
    #// @since 5.3.0
    #// 
    #// @param WP_REST_Request $request
    #// @return array|WP_Error
    #//
    def insert_attachment(self, request=None):
        
        #// Get the file via $_FILES or raw data.
        files = request.get_file_params()
        headers = request.get_headers()
        if (not php_empty(lambda : files)):
            file = self.upload_from_file(files, headers)
        else:
            file = self.upload_from_data(request.get_body(), headers)
        # end if
        if is_wp_error(file):
            return file
        # end if
        name = wp_basename(file["file"])
        name_parts = pathinfo(name)
        name = php_trim(php_substr(name, 0, -1 + php_strlen(name_parts["extension"])))
        url = file["url"]
        type = file["type"]
        file = file["file"]
        #// Include image functions to get access to wp_read_image_metadata().
        php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
        #// Use image exif/iptc data for title and caption defaults if possible.
        image_meta = wp_read_image_metadata(file)
        if (not php_empty(lambda : image_meta)):
            if php_empty(lambda : request["title"]) and php_trim(image_meta["title"]) and (not php_is_numeric(sanitize_title(image_meta["title"]))):
                request["title"] = image_meta["title"]
            # end if
            if php_empty(lambda : request["caption"]) and php_trim(image_meta["caption"]):
                request["caption"] = image_meta["caption"]
            # end if
        # end if
        attachment = self.prepare_item_for_database(request)
        attachment.post_mime_type = type
        attachment.guid = url
        if php_empty(lambda : attachment.post_title):
            attachment.post_title = php_preg_replace("/\\.[^.]+$/", "", wp_basename(file))
        # end if
        #// $post_parent is inherited from $attachment['post_parent'].
        id = wp_insert_attachment(wp_slash(attachment), file, 0, True)
        if is_wp_error(id):
            if "db_update_error" == id.get_error_code():
                id.add_data(Array({"status": 500}))
            else:
                id.add_data(Array({"status": 400}))
            # end if
            return id
        # end if
        attachment = get_post(id)
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
        do_action("rest_insert_attachment", attachment, request, True)
        return Array({"attachment_id": id, "file": file})
    # end def insert_attachment
    #// 
    #// Updates a single attachment.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, WP_Error object on failure.
    #//
    def update_item(self, request=None):
        
        if (not php_empty(lambda : request["post"])) and php_in_array(get_post_type(request["post"]), Array("revision", "attachment"), True):
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", __("Invalid parent type."), Array({"status": 400})))
        # end if
        response = super().update_item(request)
        if is_wp_error(response):
            return response
        # end if
        response = rest_ensure_response(response)
        data = response.get_data()
        if (php_isset(lambda : request["alt_text"])):
            update_post_meta(data["id"], "_wp_attachment_image_alt", request["alt_text"])
        # end if
        attachment = get_post(request["id"])
        fields_update = self.update_additional_fields_for_object(attachment, request)
        if is_wp_error(fields_update):
            return fields_update
        # end if
        request.set_param("context", "edit")
        #// This action is documented in wp-includes/rest-api/endpoints/class-wp-rest-attachments-controller.php
        do_action("rest_after_insert_attachment", attachment, request, False)
        response = self.prepare_item_for_response(attachment, request)
        response = rest_ensure_response(response)
        return response
    # end def update_item
    #// 
    #// Performs post processing on an attachment.
    #// 
    #// @since 5.3.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return WP_REST_Response|WP_Error Response object on success, WP_Error object on failure.
    #//
    def post_process_item(self, request=None):
        
        for case in Switch(request["action"]):
            if case("create-image-subsizes"):
                php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
                wp_update_image_subsizes(request["id"])
                break
            # end if
        # end for
        request["context"] = "edit"
        return self.prepare_item_for_response(get_post(request["id"]), request)
    # end def post_process_item
    #// 
    #// Checks if a given request can perform post processing on an attachment.
    #// 
    #// @sicne 5.3.0
    #// 
    #// @param WP_REST_Request $request Full details about the request.
    #// @return true|WP_Error True if the request has access to update the item, WP_Error object otherwise.
    #//
    def post_process_item_permissions_check(self, request=None):
        
        return self.update_item_permissions_check(request)
    # end def post_process_item_permissions_check
    #// 
    #// Prepares a single attachment for create or update.
    #// 
    #// @since 4.7.0
    #// 
    #// @param WP_REST_Request $request Request object.
    #// @return stdClass|WP_Error Post object.
    #//
    def prepare_item_for_database(self, request=None):
        
        prepared_attachment = super().prepare_item_for_database(request)
        #// Attachment caption (post_excerpt internally).
        if (php_isset(lambda : request["caption"])):
            if php_is_string(request["caption"]):
                prepared_attachment.post_excerpt = request["caption"]
            elif (php_isset(lambda : request["caption"]["raw"])):
                prepared_attachment.post_excerpt = request["caption"]["raw"]
            # end if
        # end if
        #// Attachment description (post_content internally).
        if (php_isset(lambda : request["description"])):
            if php_is_string(request["description"]):
                prepared_attachment.post_content = request["description"]
            elif (php_isset(lambda : request["description"]["raw"])):
                prepared_attachment.post_content = request["description"]["raw"]
            # end if
        # end if
        if (php_isset(lambda : request["post"])):
            prepared_attachment.post_parent = php_int(request["post"])
        # end if
        return prepared_attachment
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
    def prepare_item_for_response(self, post=None, request=None):
        
        response = super().prepare_item_for_response(post, request)
        fields = self.get_fields_for_response(request)
        data = response.get_data()
        if php_in_array("description", fields, True):
            data["description"] = Array({"raw": post.post_content, "rendered": apply_filters("the_content", post.post_content)})
        # end if
        if php_in_array("caption", fields, True):
            #// This filter is documented in wp-includes/post-template.php
            caption = apply_filters("get_the_excerpt", post.post_excerpt, post)
            #// This filter is documented in wp-includes/post-template.php
            caption = apply_filters("the_excerpt", caption)
            data["caption"] = Array({"raw": post.post_excerpt, "rendered": caption})
        # end if
        if php_in_array("alt_text", fields, True):
            data["alt_text"] = get_post_meta(post.ID, "_wp_attachment_image_alt", True)
        # end if
        if php_in_array("media_type", fields, True):
            data["media_type"] = "image" if wp_attachment_is_image(post.ID) else "file"
        # end if
        if php_in_array("mime_type", fields, True):
            data["mime_type"] = post.post_mime_type
        # end if
        if php_in_array("media_details", fields, True):
            data["media_details"] = wp_get_attachment_metadata(post.ID)
            #// Ensure empty details is an empty object.
            if php_empty(lambda : data["media_details"]):
                data["media_details"] = php_new_class("stdClass", lambda : stdClass())
            elif (not php_empty(lambda : data["media_details"]["sizes"])):
                for size,size_data in data["media_details"]["sizes"]:
                    if (php_isset(lambda : size_data["mime-type"])):
                        size_data["mime_type"] = size_data["mime-type"]
                        size_data["mime-type"] = None
                    # end if
                    #// Use the same method image_downsize() does.
                    image_src = wp_get_attachment_image_src(post.ID, size)
                    if (not image_src):
                        continue
                    # end if
                    size_data["source_url"] = image_src[0]
                # end for
                full_src = wp_get_attachment_image_src(post.ID, "full")
                if (not php_empty(lambda : full_src)):
                    data["media_details"]["sizes"]["full"] = Array({"file": wp_basename(full_src[0]), "width": full_src[1], "height": full_src[2], "mime_type": post.post_mime_type, "source_url": full_src[0]})
                # end if
            else:
                data["media_details"]["sizes"] = php_new_class("stdClass", lambda : stdClass())
            # end if
        # end if
        if php_in_array("post", fields, True):
            data["post"] = php_int(post.post_parent) if (not php_empty(lambda : post.post_parent)) else None
        # end if
        if php_in_array("source_url", fields, True):
            data["source_url"] = wp_get_attachment_url(post.ID)
        # end if
        if php_in_array("missing_image_sizes", fields, True):
            php_include_file(ABSPATH + "wp-admin/includes/image.php", once=True)
            data["missing_image_sizes"] = php_array_keys(wp_get_missing_image_subsizes(post.ID))
        # end if
        context = request["context"] if (not php_empty(lambda : request["context"])) else "view"
        data = self.filter_response_by_context(data, context)
        links = response.get_links()
        #// Wrap the data in a response object.
        response = rest_ensure_response(data)
        for rel,rel_links in links:
            for link in rel_links:
                response.add_link(rel, link["href"], link["attributes"])
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
        return apply_filters("rest_prepare_attachment", response, post, request)
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
        schema = super().get_item_schema()
        schema["properties"]["alt_text"] = Array({"description": __("Alternative text to display when attachment is not displayed."), "type": "string", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": "sanitize_text_field"})})
        schema["properties"]["caption"] = Array({"description": __("The attachment caption."), "type": "object", "context": Array("view", "edit", "embed"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Caption for the attachment, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML caption for the attachment, transformed for display."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})})})
        schema["properties"]["description"] = Array({"description": __("The attachment description."), "type": "object", "context": Array("view", "edit"), "arg_options": Array({"sanitize_callback": None, "validate_callback": None})}, {"properties": Array({"raw": Array({"description": __("Description for the object, as it exists in the database."), "type": "string", "context": Array("edit")})}, {"rendered": Array({"description": __("HTML description for the object, transformed for display."), "type": "string", "context": Array("view", "edit"), "readonly": True})})})
        schema["properties"]["media_type"] = Array({"description": __("Attachment type."), "type": "string", "enum": Array("image", "file"), "context": Array("view", "edit", "embed"), "readonly": True})
        schema["properties"]["mime_type"] = Array({"description": __("The attachment MIME type."), "type": "string", "context": Array("view", "edit", "embed"), "readonly": True})
        schema["properties"]["media_details"] = Array({"description": __("Details about the media file, specific to its type."), "type": "object", "context": Array("view", "edit", "embed"), "readonly": True})
        schema["properties"]["post"] = Array({"description": __("The ID for the associated post of the attachment."), "type": "integer", "context": Array("view", "edit")})
        schema["properties"]["source_url"] = Array({"description": __("URL to the original attachment file."), "type": "string", "format": "uri", "context": Array("view", "edit", "embed"), "readonly": True})
        schema["properties"]["missing_image_sizes"] = Array({"description": __("List of the missing image sizes of the attachment."), "type": "array", "items": Array({"type": "string"})}, {"context": Array("edit"), "readonly": True})
        schema["properties"]["password"] = None
        self.schema = schema
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
    def upload_from_data(self, data=None, headers=None):
        
        if php_empty(lambda : data):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_data", __("No data supplied."), Array({"status": 400})))
        # end if
        if php_empty(lambda : headers["content_type"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_content_type", __("No Content-Type supplied."), Array({"status": 400})))
        # end if
        if php_empty(lambda : headers["content_disposition"]):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_content_disposition", __("No Content-Disposition supplied."), Array({"status": 400})))
        # end if
        filename = self.get_filename_from_disposition(headers["content_disposition"])
        if php_empty(lambda : filename):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_invalid_disposition", __("Invalid Content-Disposition supplied. Content-Disposition needs to be formatted as `attachment; filename=\"image.png\"` or similar."), Array({"status": 400})))
        # end if
        if (not php_empty(lambda : headers["content_md5"])):
            content_md5 = php_array_shift(headers["content_md5"])
            expected = php_trim(content_md5)
            actual = php_md5(data)
            if expected != actual:
                return php_new_class("WP_Error", lambda : WP_Error("rest_upload_hash_mismatch", __("Content hash did not match expected."), Array({"status": 412})))
            # end if
        # end if
        #// Get the content-type.
        type = php_array_shift(headers["content_type"])
        #// Include filesystem functions to get access to wp_tempnam() and wp_handle_sideload().
        php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
        #// Save the file.
        tmpfname = wp_tempnam(filename)
        fp = fopen(tmpfname, "w+")
        if (not fp):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_file_error", __("Could not open file handle."), Array({"status": 500})))
        # end if
        fwrite(fp, data)
        php_fclose(fp)
        #// Now, sideload it in.
        file_data = Array({"error": None, "tmp_name": tmpfname, "name": filename, "type": type})
        size_check = self.check_upload_size(file_data)
        if is_wp_error(size_check):
            return size_check
        # end if
        overrides = Array({"test_form": False})
        sideloaded = wp_handle_sideload(file_data, overrides)
        if (php_isset(lambda : sideloaded["error"])):
            php_no_error(lambda: unlink(tmpfname))
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_sideload_error", sideloaded["error"], Array({"status": 500})))
        # end if
        return sideloaded
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
    def get_filename_from_disposition(self, disposition_header=None):
        
        #// Get the filename.
        filename = None
        for value in disposition_header:
            value = php_trim(value)
            if php_strpos(value, ";") == False:
                continue
            # end if
            type, attr_parts = php_explode(";", value, 2)
            attr_parts = php_explode(";", attr_parts)
            attributes = Array()
            for part in attr_parts:
                if php_strpos(part, "=") == False:
                    continue
                # end if
                key, value = php_explode("=", part, 2)
                attributes[php_trim(key)] = php_trim(value)
            # end for
            if php_empty(lambda : attributes["filename"]):
                continue
            # end if
            filename = php_trim(attributes["filename"])
            #// Unquote quoted filename, but after trimming.
            if php_substr(filename, 0, 1) == "\"" and php_substr(filename, -1, 1) == "\"":
                filename = php_substr(filename, 1, -1)
            # end if
        # end for
        return filename
    # end def get_filename_from_disposition
    #// 
    #// Retrieves the query params for collections of attachments.
    #// 
    #// @since 4.7.0
    #// 
    #// @return array Query parameters for the attachment collection as an array.
    #//
    def get_collection_params(self):
        
        params = super().get_collection_params()
        params["status"]["default"] = "inherit"
        params["status"]["items"]["enum"] = Array("inherit", "private", "trash")
        media_types = self.get_media_types()
        params["media_type"] = Array({"default": None, "description": __("Limit result set to attachments of a particular media type."), "type": "string", "enum": php_array_keys(media_types)})
        params["mime_type"] = Array({"default": None, "description": __("Limit result set to attachments of a particular MIME type."), "type": "string"})
        return params
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
    def upload_from_file(self, files=None, headers=None):
        
        if php_empty(lambda : files):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_no_data", __("No data supplied."), Array({"status": 400})))
        # end if
        #// Verify hash, if given.
        if (not php_empty(lambda : headers["content_md5"])):
            content_md5 = php_array_shift(headers["content_md5"])
            expected = php_trim(content_md5)
            actual = php_md5_file(files["file"]["tmp_name"])
            if expected != actual:
                return php_new_class("WP_Error", lambda : WP_Error("rest_upload_hash_mismatch", __("Content hash did not match expected."), Array({"status": 412})))
            # end if
        # end if
        #// Pass off to WP to handle the actual upload.
        overrides = Array({"test_form": False})
        #// Bypasses is_uploaded_file() when running unit tests.
        if php_defined("DIR_TESTDATA") and DIR_TESTDATA:
            overrides["action"] = "wp_handle_mock_upload"
        # end if
        size_check = self.check_upload_size(files["file"])
        if is_wp_error(size_check):
            return size_check
        # end if
        #// Include filesystem functions to get access to wp_handle_upload().
        php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
        file = wp_handle_upload(files["file"], overrides)
        if (php_isset(lambda : file["error"])):
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_unknown_error", file["error"], Array({"status": 500})))
        # end if
        return file
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
        
        media_types = Array()
        for mime_type in get_allowed_mime_types():
            parts = php_explode("/", mime_type)
            if (not (php_isset(lambda : media_types[parts[0]]))):
                media_types[parts[0]] = Array()
            # end if
            media_types[parts[0]][-1] = mime_type
        # end for
        return media_types
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
    def check_upload_size(self, file=None):
        
        if (not is_multisite()):
            return True
        # end if
        if get_site_option("upload_space_check_disabled"):
            return True
        # end if
        space_left = get_upload_space_available()
        file_size = filesize(file["tmp_name"])
        if space_left < file_size:
            return php_new_class("WP_Error", lambda : WP_Error("rest_upload_limited_space", php_sprintf(__("Not enough space to upload. %s KB needed."), number_format(file_size - space_left / KB_IN_BYTES)), Array({"status": 400})))
        # end if
        if file_size > KB_IN_BYTES * get_site_option("fileupload_maxk", 1500):
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
