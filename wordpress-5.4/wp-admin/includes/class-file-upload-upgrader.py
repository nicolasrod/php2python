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
#// Upgrade API: File_Upload_Upgrader class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Core class used for handling file uploads.
#// 
#// This class handles the upload process and passes it as if it's a local file
#// to the Upgrade/Installer functions.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader.php.
#//
class File_Upload_Upgrader():
    package = Array()
    filename = Array()
    id = 0
    #// 
    #// Construct the upgrader for a form.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $form      The name of the form the file was uploaded from.
    #// @param string $urlholder The name of the `GET` parameter that holds the filename.
    #//
    def __init__(self, form=None, urlholder=None):
        
        if php_empty(lambda : PHP_FILES[form]["name"]) and php_empty(lambda : PHP_REQUEST[urlholder]):
            wp_die(__("Please select a file"))
        # end if
        #// Handle a newly uploaded file. Else, assume it's already been uploaded.
        if (not php_empty(lambda : PHP_FILES)):
            overrides = Array({"test_form": False, "test_type": False})
            file = wp_handle_upload(PHP_FILES[form], overrides)
            if (php_isset(lambda : file["error"])):
                wp_die(file["error"])
            # end if
            self.filename = PHP_FILES[form]["name"]
            self.package = file["file"]
            #// Construct the object array.
            object = Array({"post_title": self.filename, "post_content": file["url"], "post_mime_type": file["type"], "guid": file["url"], "context": "upgrader", "post_status": "private"})
            #// Save the data.
            self.id = wp_insert_attachment(object, file["file"])
            #// Schedule a cleanup for 2 hours from now in case of failed installation.
            wp_schedule_single_event(time() + 2 * HOUR_IN_SECONDS, "upgrader_scheduled_cleanup", Array(self.id))
        elif php_is_numeric(PHP_REQUEST[urlholder]):
            #// Numeric Package = previously uploaded file, see above.
            self.id = int(PHP_REQUEST[urlholder])
            attachment = get_post(self.id)
            if php_empty(lambda : attachment):
                wp_die(__("Please select a file"))
            # end if
            self.filename = attachment.post_title
            self.package = get_attached_file(attachment.ID)
        else:
            #// Else, It's set to something, Back compat for plugins using the old (pre-3.3) File_Uploader handler.
            uploads = wp_upload_dir()
            if (not uploads and False == uploads["error"]):
                wp_die(uploads["error"])
            # end if
            self.filename = sanitize_file_name(PHP_REQUEST[urlholder])
            self.package = uploads["basedir"] + "/" + self.filename
            if 0 != php_strpos(php_realpath(self.package), php_realpath(uploads["basedir"])):
                wp_die(__("Please select a file"))
            # end if
        # end if
    # end def __init__
    #// 
    #// Delete the attachment/uploaded file.
    #// 
    #// @since 3.2.2
    #// 
    #// @return bool Whether the cleanup was successful.
    #//
    def cleanup(self):
        
        if self.id:
            wp_delete_attachment(self.id)
        elif php_file_exists(self.package):
            return php_no_error(lambda: unlink(self.package))
        # end if
        return True
    # end def cleanup
# end class File_Upload_Upgrader
